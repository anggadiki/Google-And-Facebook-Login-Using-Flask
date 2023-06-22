from flask import Flask, redirect, request, render_template, make_response
from google_auth_oauthlib.flow import Flow
import facebook

app = Flask(__name__)

# Konfigurasi OAuth 2.0 Google
GOOGLE_CLIENT_ID = 'isi dengan Client ID Google kalian '
GOOGLE_CLIENT_SECRET = 'isi dengan Client Secret Google kalian'
GOOGLE_REDIRECT_URI = 'isi dengan URL callback Google kalian'
GOOGLE_SCOPE = 'openid email profile'

# Konfigurasi aplikasi Facebook
FACEBOOK_APP_ID = 'isi dengan ID aplikasi Facebook kalian'
FACEBOOK_APP_SECRET = 'isi dengan Secret Key aplikasi Facebook kalian'
FACEBOOK_REDIRECT_URI = 'isi dengan URL callback Facebook kalian'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    # Membuat objek Flow untuk autentikasi Google
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=[GOOGLE_SCOPE],
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    # Membuat URL autentikasi dan mengarahkan pengguna ke halaman Google
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)

@app.route('/login/facebook')
def login_facebook():
    # Membuat URL autentikasi dan mengarahkan pengguna ke halaman autentikasi Facebook
    fb = facebook.GraphAPI()
    auth_url = fb.get_auth_url(FACEBOOK_APP_ID, FACEBOOK_REDIRECT_URI)
    return redirect(auth_url)

@app.route('/callback/google')
def callback_google():
    # Memproses respons setelah pengguna berhasil melakukan autentikasi dengan Google
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=[GOOGLE_SCOPE],
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)

    # Mendapatkan informasi pengguna yang telah terautentikasi dari Google
    credentials = flow.credentials
    user_info = credentials.id_token

    # Lakukan sesuatu dengan informasi pengguna Google
    # Misalnya, kalian dapat menyimpan informasi pengguna dalam database atau membuat sesi pengguna

    response = make_response('Login successful')
    return response

@app.route('/callback/facebook')
def callback_facebook():
    # Memproses respons setelah pengguna berhasil melakukan autentikasi dengan Facebook
    code = request.args.get('code')

    # Mendapatkan access token dari kode otorisasi
    fb = facebook.GraphAPI()
    access_token = fb.get_access_token_from_code(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_REDIRECT_URI, code)

    # Mendapatkan informasi pengguna yang telah terautentikasi dari Facebook
    user_info = fb.get_user_info(access_token)

    # Lakukan sesuatu dengan informasi pengguna Facebook
    # Misalnya, kalian dapat menyimpan informasi pengguna dalam database atau membuat sesi pengguna

    response = make_response('Login successful')
    return response

if __name__ == '__main__':
    app.run(debug=True)
