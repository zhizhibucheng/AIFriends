const platform = 'cloud'

const CONFIG_API = {
    HTTP_URL:'',
    VAD_URL:'',
    MODEL_BASE_URL: '',
}

if (platform === 'vue') {
    CONFIG_API.HTTP_URL = 'http://127.0.0.1:8000'
    CONFIG_API.VAD_URL = 'http://localhost:5173/vad/'
    CONFIG_API.MODEL_BASE_URL = ''
}else if(platform === 'django') {
    CONFIG_API.HTTP_URL = 'http://127.0.0.1:8000'
    CONFIG_API.VAD_URL = 'http://127.0.0.1:8000/static/frontend/vad/'
    CONFIG_API.MODEL_BASE_URL = '/static/frontend'

}else if(platform === 'cloud') {
    CONFIG_API.HTTP_URL = 'https://zhizhibuchengai.com.cn'
    CONFIG_API.VAD_URL = 'https://zhizhibuchengai.com.cn/static/frontend/vad/'
    CONFIG_API.MODEL_BASE_URL = '/static/frontend'

}

export default CONFIG_API