from dataclasses import dataclass


@dataclass
class Lab:
    '''Defines the PYTZEN DATA SCIENCE LAB attributes.
    '''

    project_name: str = 'pytzen'

    url_homepage: str = 'https://www.pytzen.com'
    url_respository: str = 'https://www.pytzen.org'
    url_github: str = 'https://github.com/pytzen'
    url_blog: str = 'https://blog.pytzen.org'
    url_linkedin: str = 'https://www.linkedin.com/company/pytzen'

    path_lab: str = '/home/pytzen/lab'
    path_data: str = '/home/pytzen/lab/data'
    path_package: str = '/home/pytzen/lab/pytzen/src'
    path_repository: str = '/home/pytzen/lab/pytzen'