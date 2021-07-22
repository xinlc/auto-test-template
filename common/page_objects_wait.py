"""
Adapted from the page-objects Python package addressing two perceived shortfalls:
 - Lack of an easy way to get at the locator for a field, for instance for waits.
 - Extra calls to driver.find_element() without any caching.

The API of this module is mostly backwards compatible with page-objects, with the following differences:
 - The `root_uri` kwarg or PageObject is deprecated in favor of `base_url`, but root_uri is still supported.
 - The behavior where setting the attribute sends keys seems to obscure the selenium bindings for selenium,
   and are too magical, so they are removed.
 - The factory methods at end are removed, because I never used it with factory methods
"""
import warnings

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

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


class PageObject(object):
    """Page Object pattern.

    :param webdriver: `selenium.webdriver.WebDriver`
        Selenium webdriver instance
    :param base_url: `str`
        Base URL to base any calls to the ``PageObject.get`` method.
    :param root_uri: `str`
        Alias for base_url during initialization
    :param caching: `bool'
        Controls whether this PageObject will be caching element instances (default True)
    :param wait: None or `WebDriverWait`
        an explicit WebDriverWait to use if needed
    """
    WAIT_TIMEOUT = 10
    POLL_DELAY = 0.1

    def __init__(self, webdriver, base_url=None, caching=True, wait=None, root_uri=None):
        self.webdriver = webdriver
        if not base_url and root_uri:
            warnings.warn('root_uri attribute is deprecated', DeprecationWarning, stacklevel=2)
            base_url = root_uri
        self.base_url = str(base_url) if base_url else ''
        self.__wait = wait
        if caching:
            self.__cache = dict()

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the base_url attribute.
        """
        self.webdriver.get(self.base_url + uri)

    def open(self, uri=None):
        if not uri:
            uri = self.URI
        self.get(uri)

    def clear_cache(self):
        self.__cache.clear()

    @classmethod
    def element_names(cls):
        return set(
            name for name, element_def in cls.__dict__.items()
            if isinstance(element_def, PageElement)
        )

    @property
    def wait(self):
        if self.__wait is None:
            self.__wait = WebDriverWait(self.webdriver, self.WAIT_TIMEOUT, self.POLL_DELAY)
        return self.__wait

    @classmethod
    def locator_for(cls, name):
        element_def = getattr(cls, name, None)
        if not isinstance(element_def, PageElement):
            raise ValueError('%s: no such element is defined' % name)
        return element_def.locator

    def wait_for(self, *elements):
        for name in elements:
            element_def = getattr(type(self), name, None)
            if not isinstance(element_def, PageElement):
                raise ValueError('%s: no such element is defined' % name)
        for name in elements:
            element_def = getattr(type(self), name, None)
            if isinstance(element_def, MultiPageElement):
                self.wait.until(expected_conditions.visibility_of_any_elements_located(element_def.locator))
            else:
                self.wait.until(expected_conditions.visibility_of_element_located(element_def.locator))

    def wait_for_all(self):
        return self.wait_for(*self.element_names())


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

    :param caching: `bool`
        This element will be cached or will not be cached (default True)
    :param context: `bool`
        This element is expected to be called with context

    Page Elements are used to access elements on a page. The are constructed
    using this factory method to specify the locator for the element.

        >>> from page_objects import PageObject, PageElement
        >>> class MyPage(PageObject):
                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')

    Page Elements act as property descriptors for their Page Object, you can get
    them as normal attributes.
    """

    def __init__(self, context=False, caching=True, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))
        self.locator = (_LOCATOR_MAP[k], v)
        self.caching = caching
        self.has_context = bool(context)

    def find(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def __get__(self, instance, owner, context=None):
        if not instance:
            return self
        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)
        if not context:
            context = instance.webdriver
        instance_cache = getattr(instance, '_PageObject__cache', None)
        if self.caching and instance_cache is not None:
            value = instance_cache.get(self, None)
            if not value:
                instance_cache[self] = value = self.find(context)
            return value
        return self.find(context)

    def __set__(self, instance, value):
        raise ValueError('Cannot set page element value any longer')


class MultiPageElement(PageElement):
    """ Like `PageElement` but returns multiple results.

        >>> from page_objects import PageObject, MultiPageElement
        >>> class MyPage(PageObject):
                all_table_rows = MultiPageElement(tag='tr')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(tag='tr', context=True)

    """

    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []
