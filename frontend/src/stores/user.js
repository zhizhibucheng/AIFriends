import {defineStore}  from "pinia";
import {ref} from "vue";

export const useUserStore =defineStore('user',()=>{
    const id = ref(0)
    const username = ref('')
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')
    const hasPulledUserInfo = ref(false)
    const DEFAULT_BACKGROUND = '/media/user/app_backgrounds/default.jpg'

    const appBackground = ref(DEFAULT_BACKGROUND)

    const isVerified = ref(false)
    const isMinor = ref(false)

    function setAppBackground(newBackground) {
        appBackground.value = newBackground
    }

    function restoreDefaultBackground() {
        appBackground.value = DEFAULT_BACKGROUND
    }

    function isLogin(){
        return !!accessToken.value
    }

    function setAccessToken(token){
        accessToken.value = token
    }

    function setUserInfo(data){
        id.value = data.user_id
        username.value = data.username
        photo.value=data.photo
        profile.value=data.profile

        isVerified.value = data.is_verified || false
        isMinor.value = data.is_minor || false

        if (data.app_background) {
            let bgUrl = data.app_background;

            // 【修复开始】: 如果是带有 http/https 的绝对路径，转换为相对路径
            if (bgUrl.startsWith('http')) {
                try {
                    const urlObj = new URL(bgUrl);
                    bgUrl = urlObj.pathname; // 只提取 '/media/user/app_backgrounds/xxx.jpg'
                } catch (e) {
                    console.error('Invalid URL:', bgUrl);
                }
            }
            // 【修复结束】

            if (bgUrl.endsWith(DEFAULT_BACKGROUND)) {
                 // 如果以默认背景结尾，保持 DEFAULT_BACKGROUND 不变
                 appBackground.value = DEFAULT_BACKGROUND;
            } else {
                 appBackground.value = bgUrl;
            }
        }
    }

    function logout(){
        id.value = 0
        username.value = ''
        photo.value = ''
        accessToken.value = ''
        profile.value = ''
        appBackground.value = DEFAULT_BACKGROUND

        isVerified.value = false
        isMinor.value = false
    }

    function setHasPulledUserInfo(newStatus){
        hasPulledUserInfo.value = newStatus
    }

    function setVerifyStatus(verified, minor) {
        isVerified.value = verified
        isMinor.value = minor
    }

    return {
        id,
        username,
        photo,
        accessToken,
        setAccessToken,
        profile,
        setUserInfo,
        logout,
        isLogin,
        hasPulledUserInfo,
        setHasPulledUserInfo,
        appBackground,
        setAppBackground,
        restoreDefaultBackground,
        isVerified,
        isMinor,
        setVerifyStatus, // 导出新方法
    }
})