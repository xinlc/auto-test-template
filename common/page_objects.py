"""POM设计模式

增强 page-objects 库，原仓库地址：https://github.com/man-group/page-objects

- 增加 GroupPageElement
- 支持 延迟等待
- context 支持字符串，传入元素变量名即可，并兼容bool写法

"""

__author__ = 'Richard'
__version__ = '2021-07-18'

from typing import Union
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Map PageElement constructor arguments to webdriver locator enums
_LOCATOR_MAP = {'css': By.CSS_SELECTOR,
                'id_': By.ID,
                'name': By.NAME,
                'xpath': By.XPATH,
                'link_text': By.LINK_TEXT,
                'partial_link_text': By.PARTIAL_LINK_TEXT,
                'tag_name': By.TAG_NAME,
                'class_name': By.CLASS_NAME,
                }

# Number of seconds before timing out
_WAIT_TIMEOUT = 10
# How long to sleep inbetween calls to the method
_POLL_DELAY = 0.5


class PageObject(object):
    """Page Object pattern.

    :param webdriver: `selenium.webdriver.WebDriver`
        Selenium webdriver instance
    :param root_uri: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
    """

    def __init__(self, webdriver, root_uri=None, default_timeout=_WAIT_TIMEOUT, default_poll_delay=_POLL_DELAY):
        self.w = webdriver
        self.root_uri = root_uri if root_uri else getattr(self.w, 'root_uri', None)
        self.default_timeout = default_timeout
        self.default_poll_delay = default_poll_delay

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.w.get(root_uri + uri)


class PageElement(object):
    """Page Element descriptor.

    :param css:    `str`
        Use this css locator
    :param id_:    `str`
        Use this element ID locator
    :param name:    `str`
        Use this element name locator
    :param xpath:    `str`
        Use this xpath locator
    :param link_text:    `str`
        Use this link text locator
    :param partial_link_text:    `str`
        Use this partial link text locator
    :param tag_name:    `str`
        Use this tag name locator
    :param class_name:    `str`
        Use this class locator

    :param context: `bool | str`
        This element is expected to be called with context

    Page Elements are used to access elements on a page. The are constructed
    using this factory method to specify the locator for the element.

        >>> from page_objects import PageObject, PageElement
        >>> class MyPage(PageObject):
                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(name='bar', context=True)
                    usage: elem1(elem_with_context).text
                elem_with_elem1 = PageElement(name='bar', context='elem1')
                    usage: elem_with_elem1.text

    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """

    def __init__(self, context: Union[bool, str] = None, timeout=None, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))
        self.locator = (_LOCATOR_MAP[k], v)
        # 是 bool 类型上下文
        self.has_context = isinstance(context, bool) and context
        self._context = context
        self.timeout = timeout

    def wait_for(self, instance, method):
        t = instance.default_timeout if self.timeout is None else self.timeout
        return WebDriverWait(instance.w, t, poll_frequency=instance.default_poll_delay).until(method)

    def find(self, instance, context):
        try:
            return self.wait_for(instance, lambda driver: context.find_element(*self.locator))
            # 等待条件改为可见元素, 避免元素还未渲染完成返回，如果就是要获取隐藏元素，单独写查询吧
            # return self.wait_for(instance, lambda driver: EC.visibility_of_element_located(self.locator)(context))
        except NoSuchElementException:
            return None

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None

        # if not context and self.has_context:
        #     return lambda ctx: self.__get__(instance, owner, context=ctx)

        # if not context:
        #     context = instance.w

        if not context:
            if self.has_context:
                return lambda ctx: self.__get__(instance, owner, context=ctx)
            elif self._context:
                context = instance.__getattribute__(self._context)
            else:
                context = instance.w

        return self.find(instance, context)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


class MultiPageElement(PageElement):
    """ Like `PageElement` but returns multiple results.

        >>> from page_objects import PageObject, MultiPageElement
        >>> class MyPage(PageObject):
                all_table_rows = MultiPageElement(tag='tr')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(tag='tr', context=True)
    """

    def find(self, instance, context):
        try:
            return self.wait_for(instance, lambda driver: context.find_elements(*self.locator))
            # 等待条件改为可见元素, 避免元素还未渲染完成返回，如果就是要获取隐藏元素，单独写查询吧
            # return self.wait_for(instance, lambda driver: EC.visibility_of_any_elements_located(self.locator)(context))
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


class GroupPageElement(MultiPageElement):
    """
    get a group elements.like combox and so on
    return is a  dic{}
    exp.
    <select class="search_input" id="level" name="level">
        <option value="">select</option>
        <option value="5">6</option>
        <option value="6">7</option>
        <option value="7">8</option>
        <option value="8">9</option>
        <option value="9">10</option>
    </select>

    merviewlevel=GroupPageElement(xpath='//*[@id="level"]/option')


    merviewlevel[u'6'].click()

    PS:the selecter xpath is the best
    """

    def find(self, instance, context):
        try:
            dic_group = {}
            elements = self.wait_for(instance, lambda driver: context.find_elements(*self.locator))
            # 等待条件改为可见元素, 避免元素还未渲染完成返回，如果就是要获取隐藏元素，单独写查询吧
            # elements = self.wait_for(instance,
            #                          lambda driver: EC.visibility_of_any_elements_located(self.locator)(context))
            for aElement in elements:
                dic_group[aElement.text] = aElement
            return dic_group

        except NoSuchElementException:
            return {}

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


# Backwards compatibility with previous versions that used factory methods
page_element = PageElement
multi_page_element = MultiPageElement
group_page_element = GroupPageElement
