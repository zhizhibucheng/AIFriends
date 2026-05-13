// 角色配置文件，未来加新角色只需在这里加一段即可
import CONFIG_API from '@/js/config/config.js';
export const AVATAR_CONFIG = {
  // 当前的男孩
  male: {
    modelPath: `${CONFIG_API.MODEL_BASE_URL}/models/boyall.glb`,
    targetHeight: 2.1,     // 模型缩放高度
    speed: 60,             // 移动速度 (像素/秒)
    animations: {
      entry: 'jump',       // 出场动作
      idle: 'idle',        // 待机动作
      move: 'walk'         // 移动动作
    }
  },

  // 未来的女孩示例
  female: {
    modelPath: `${CONFIG_API.MODEL_BASE_URL}/models/girlall.glb`,
    targetHeight: 2.1,
    speed: 55,
    animations: {
      entry: 'greet',
      idle: 'think',
      move: 'run'
    }
  },

  // 未来的宠物狗示例
  dog: {
    modelPath: '/static/frontend/models/dog.glb',
    targetHeight: 1.5,
    speed: 90,
    animations: {
      entry: 'bark',
      idle: 'sit',
      move: 'trot'
    }
  }
};