import {defineStore}  from "pinia";
import {ref} from "vue";

export const useUserStore =defineStore('user',()=>{
    const id = ref(0)
    const username = ref('')
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')
    const hasPulledUserInfo = ref(false)
    const DEFAULT_BACKGROUND = '/media/user/app_backgrounds/default.png'

    const appBackground = ref(DEFAULT_BACKGROUND)

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

        if (data.app_background) {
            appBackground.value = data.app_background
        }
    }

    function logout(){
        id.value = 0
        username.value = ''
        photo.value = ''
        accessToken.value = ''
        profile.value = ''
        appBackground.value = DEFAULT_BACKGROUND
    }

    function setHasPulledUserInfo(newStatus){
        hasPulledUserInfo.value = newStatus
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
    }
})