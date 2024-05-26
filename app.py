import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_auth
import boto3
import dash_uploader as du
import os 
import ast
# Keep this out of source code repository - save in a file or a database
#secretparser=configparser.ConfigParser()
#secretparser.read('confi.ini')
session=boto3.Session(aws_access_key_id = os.environ["AWS_ACCESS_KEY"], aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"], region_name = os.environ["REGION_NAME"])



#session = boto3.Session()
ssm = session.client('ssm')
PlotlyDashOAuth = ssm.get_parameter(Name='PlotlyDashOAuth', WithDecryption=False)
PWPAIR = ast.literal_eval(PlotlyDashOAuth['Parameter']['Value'])
VALID_USERNAME_PASSWORD_PAIRS = PWPAIR


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SOLAR],suppress_callback_exceptions = True)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

#Configure the Dash-Uploader
UPLOAD_FOLDER_ROOT = os.path.join(os.path.dirname(__file__),"uploads")
#print(UPLOAD_FOLDER_ROOT)
du.configure_upload(app, UPLOAD_FOLDER_ROOT)
#print(filelist = dir(fullfile(os.path.join(os.path.dirname(__file__),"uploads"), '**\*.*')))





app.layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([

        ]),
        dbc.Col([
               html.H1('Master Analytics Platform - Our Solutions Catalog'),    
        ]),
        dbc.Col([

        ]),
    ]),
    
    html.Br(),
    dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Chose the solution you need",
    color="primary",
    dark=True,
    className="mb-2",
    ),

    dash.page_container
])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)