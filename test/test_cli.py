from click.testing import CliRunner
from cfa.url import url
from cfa.main import create_flask_app

# just initial testing

def test_url_list():
    """test url_list data type is a dict"""
    assert type(url) == dict

def test_template_list_command():
    """test list command"""
    runner = CliRunner()
    result = runner.invoke(create_flask_app,["list"])
    
    assert result.exit_code == 0
    assert "available templates:" in result.output
    assert "»" in result.output    