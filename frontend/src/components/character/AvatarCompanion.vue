<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { AVATAR_CONFIG } from '@/config/avatarConfig.js';

const props = defineProps({
  avatarType: {
    type: String,
    default: 'none'
  }
});

const containerRef = ref(null);

// 动态容器尺寸，手机端设置为120，电脑端200
const containerSize = ref(window.innerWidth < 640 ? 120 : 200);

let scene, camera, renderer, mixer, wrapper;
let animationId;
let actions = {};
let previousTime = 0;

let currentStateName = null;
let currentAction = null;
let wanderTimer = null;
let moveAngle = Math.random() * Math.PI * 2;

// 🚀 性能优化 1：去掉 ref()，不再让 Vue 参与 60fps 的高频计算
let posX = window.innerWidth / 2;
let posY = window.innerHeight / 2;

let charConfig = null;

onMounted(() => {
  if (props.avatarType === 'none' || !props.avatarType) return;
  charConfig = AVATAR_CONFIG[props.avatarType] || AVATAR_CONFIG['male'];

  setInitialPosition();
  initThreeJS();
  window.addEventListener('resize', onWindowResize);
});

onBeforeUnmount(() => {
  if (animationId) cancelAnimationFrame(animationId);
  if (wanderTimer) clearTimeout(wanderTimer);
  if (renderer) renderer.dispose();
  if (scene) scene.clear();
  window.removeEventListener('resize', onWindowResize);
});

function setInitialPosition() {
  const isMobile = window.innerWidth < 640;
  if (isMobile) {
    // 手机端居中出生，防止一开始就在边缘卡住
    posX = window.innerWidth * 0.25;
    posY = window.innerHeight * 0.15;
  } else {
    posX = window.innerWidth / 2 + 300;
    posY = window.innerHeight - 150;
  }
  // 初始化时立刻应用一次位置
  if (containerRef.value) {
    containerRef.value.style.transform = `translate3d(${posX}px, ${posY}px, 0)`;
  }
}

function onWindowResize() {
  if (!renderer || !camera) return;
  camera.updateProjectionMatrix();
  // 屏幕旋转或缩放时同步更新边界和画布大小
  containerSize.value = window.innerWidth < 640 ? 120 : 200;
  renderer.setSize(containerSize.value, containerSize.value, false);
}

function initThreeJS() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
  camera.position.set(0, 0, 5);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  // 使用动态的容器尺寸
  renderer.setSize(containerSize.value, containerSize.value, false);
  renderer.setPixelRatio(window.devicePixelRatio);
  containerRef.value.appendChild(renderer.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff, 2.5);
  scene.add(ambientLight);
  const directionalLight = new THREE.DirectionalLight(0xffffff, 2.0);
  directionalLight.position.set(2, 5, 3);
  scene.add(directionalLight);

  const loader = new GLTFLoader();
  const dracoLoader = new DRACOLoader();
  // 使用 Google 官方的 CDN 解码库，不需要本地下载任何多余文件
  dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
  loader.setDRACOLoader(dracoLoader);

  loader.load(charConfig.modelPath, (gltf) => {
    const model = gltf.scene;
    const box = new THREE.Box3().setFromObject(model);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    wrapper = new THREE.Group();
    model.position.set(-center.x, -center.y, -center.z);
    wrapper.add(model);

    // 核心修改点：手机端按比例再缩小模型，防止显得过大
    const isMobile = window.innerWidth < 640;
    const baseHeight = charConfig.targetHeight || 3.0;
    const targetHeight = isMobile ? baseHeight * 0.85 : baseHeight; // 手机端缩放至 85%

    const scaleFactor = size.y > 0 ? targetHeight / size.y : 1;
    wrapper.scale.set(scaleFactor, scaleFactor, scaleFactor);
    scene.add(wrapper);

    mixer = new THREE.AnimationMixer(model);
    gltf.animations.forEach((clip) => {
      clip.tracks = clip.tracks.filter(track => !track.name.includes('.scale'));
      actions[clip.name] = mixer.clipAction(clip);
    });

    startSpawnSequence();
  }, undefined, (error) => {
    console.error(`模型加载失败:`, error);
  });

  animate();
}

function startSpawnSequence() {
  const entryAnimName = charConfig.animations.entry;
  const idleAnimName = charConfig.animations.idle;

  const spawnAction = actions[entryAnimName];
  const idleAction = actions[idleAnimName];

  if (spawnAction && idleAction) {
    spawnAction.setLoop(THREE.LoopOnce);
    spawnAction.clampWhenFinished = true;
    currentAction = spawnAction;
    spawnAction.play();
    mixer.addEventListener('finished', (e) => {
      if (e.action === spawnAction) wanderLoop('idle');
    });
  } else {
    wanderLoop('idle');
  }
}

function wanderLoop(state) {
  currentStateName = state;
  const animName = charConfig.animations[state];
  const nextAction = actions[animName] || actions[Object.keys(actions)[0]];
  if (!nextAction) return;

  if (currentAction && currentAction !== nextAction) {
    nextAction.reset().play();
    currentAction.crossFadeTo(nextAction, 0.4, true);
  } else {
    nextAction.play();
  }
  currentAction = nextAction;

  if (state === 'move') {
    moveAngle += (Math.random() * Math.PI / 1.5 - Math.PI / 3);
  }

  const duration = state === 'idle' ? Math.random() * 3000 + 3000 : Math.random() * 4000 + 2000;
  wanderTimer = setTimeout(() => {
    const hasMoveAnim = !!actions[charConfig.animations.move];
    wanderLoop(state === 'idle' && hasMoveAnim ? 'move' : 'idle');
  }, duration);
}

function animate(time) {
  animationId = requestAnimationFrame(animate);
  const delta = previousTime === 0 ? 0 : Math.min((time - previousTime) / 1000, 0.1);
  previousTime = time;

  if (mixer) mixer.update(delta);

  if (wrapper && containerRef.value) {
    if (currentStateName === 'move') {
      posX += Math.cos(moveAngle) * charConfig.speed * delta;
      posY += Math.sin(moveAngle) * charConfig.speed * delta;

      // 使用动态的 margin 限制边界，根据画布大小自适应，防止人物走出屏幕
      const margin = containerSize.value / 2;
      let hitEdge = false;

      if (posX > window.innerWidth - margin) {
          posX = window.innerWidth - margin;
          hitEdge = true;
      } else if (posX < margin) {
          posX = margin;
          hitEdge = true;
      }

      if (posY > window.innerHeight - margin) {
          posY = window.innerHeight - margin;
          hitEdge = true;
      } else if (posY < margin) {
          posY = margin;
          hitEdge = true;
      }

      if (hitEdge) {
          const angleToCenter = Math.atan2(
            window.innerHeight / 2 - posY,
            window.innerWidth / 2 - posX
          );
          moveAngle = angleToCenter + (Math.random() * Math.PI / 2 - Math.PI / 4);

          clearTimeout(wanderTimer);
          wanderLoop('idle');
      }

      const targetRotation = -moveAngle + Math.PI / 2;
      wrapper.rotation.y += (targetRotation - wrapper.rotation.y) * 5 * delta;

    } else if (currentStateName === 'idle') {
      wrapper.rotation.y += (0 - wrapper.rotation.y) * 2 * delta;
    }

    // 🚀 性能优化 2：直接操作 DOM 的 translate3d，开启 GPU 硬件加速，极其丝滑
    containerRef.value.style.transform = `translate3d(${posX}px, ${posY}px, 0)`;
  }

  renderer.render(scene, camera);
}
</script>

<template>
  <div
    v-show="props.avatarType !== 'none'"
    ref="containerRef"
    class="avatar-companion-container"
    :style="{
      width: containerSize + 'px',
      height: containerSize + 'px',
      marginLeft: -(containerSize / 2) + 'px',
      marginTop: -(containerSize / 2) + 'px'
    }"
  ></div>
</template>

<style scoped>
.avatar-companion-container {
  position: fixed;
  left: 0;
  top: 0;
  pointer-events: none;
  z-index: 999999;
  /* 强制告诉浏览器这个元素会发生位移变换，提前做好 GPU 渲染准备 */
  will-change: transform;
}
</style>