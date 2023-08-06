# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwhtmltopdf']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'playwright']

setup_kwargs = {
    'name': 'pwhtmltopdf',
    'version': '0.1.3',
    'description': 'playwright render html to pdf',
    'long_description': '# Playwright HTML to PDF\n\nA modern html to pdf scheme based on playwright, Support more html and css technologies\n\n## Installation\n\n1. Install pwhtmltopdf\n    ```py\n   pip install pwhtmltopdf\n   ```\n2. Install chromium\n   ```sh\n   playwright install chromium\n   ```\n\n## Usage\n\nSimple example:\n\n```python\nimport asyncio\nimport pathlib\nfrom pwhtmltopdf import HtmlToPdf\n\n\nasync def this_from_url():\n    htp = HtmlToPdf()\n    await htp.from_url("https://playwright.dev/", "from_url.pdf")\n    await htp.close()\n\n\nasync def this_from_file():\n    htp = HtmlToPdf()\n    # Make sure the current directory has a test.html file\n    await htp.from_file("test.html", "from_file.pdf")\n    await htp.close()\n\n\nasync def this_from_string():\n    htp = HtmlToPdf()\n    content = pathlib.Path("test.html").read_text()\n    await htp.from_string(content, "from_string.pdf")\n    await htp.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(this_from_url())\n```\n\nRender fill:\n\nWhen `local_render` is equal to true, jinja2 template syntax will be used to render filled html,\nIf html needs to use local static resources, you need to set `static_root`,\nIf you want to render filled data dynamically to generate pdf(Based on jinja2), try the following method👇\n```python\nimport asyncio\nimport pathlib\nfrom pwhtmltopdf import HtmlToPdf\n\n\nasync def this_render_from_url():\n    file_path = pathlib.Path("tests/images.html").absolute()\n    htp = HtmlToPdf(static_root="tests/static")\n    await htp.from_url(\n        f"file://{file_path}",\n        "tests/effect/from_url/local_url_render.pdf",\n        local_render=True,\n        char_code=123,\n    )\n    await htp.close()\n\n\nasync def this_render_from_file():\n    htp = HtmlToPdf(static_root="tests/static")\n    await htp.from_file(\n        "tests/images.html", "tests/effect/from_file/images_render.pdf", local_render=True, char_code=123\n    )\n    await htp.close()\n\n\nasync def this_render_from_string():\n    content = pathlib.Path("tests/images.html").read_text()\n    htp = HtmlToPdf(static_root="tests/static")\n    await htp.from_string(content, "tests/effect/from_string/images_render.pdf", local_render=True, char_code=123)\n    await htp.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(this_render_from_url())\n```\n',
    'author': 'vvanglro',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vvanglro/pwhtmltopdf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
