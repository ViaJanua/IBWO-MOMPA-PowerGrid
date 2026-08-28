<template>
  <div ref="containerRef" class="three-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const containerRef = ref(null);
let scene = null;
let camera = null;
let renderer = null;
let controls = null;
let model = null;
let animationId = null;

// 加载模型
const loadModel = (loader) => {

  const modelPath = '/src/assets/models/grid_model.glb';
  
  loader.load(
    modelPath,
    (gltf) => {
      model = gltf.scene;
      scene.add(model);
      console.log(' 3D模型加载成功');
    },
    (xhr) => {
      const progress = (xhr.loaded / xhr.total * 100).toFixed(0);
      console.log(` 模型加载进度: ${progress}%`);
    },
    (error) => {
      console.error(' 模型加载失败:', error);
      // 模型加载失败，创建备用场景
      createFallbackScene();
    }
  );
};

// 备用场景
const createFallbackScene = () => {
  const geometry = new THREE.BoxGeometry(2, 2, 2);
  const material = new THREE.MeshStandardMaterial({ color: 0x2b6cb0, metalness: 0.3, roughness: 0.4 });
  const cube = new THREE.Mesh(geometry, material);
  scene.add(cube);
  
  // 添加网格辅助线
  const gridHelper = new THREE.GridHelper(10, 10);
  scene.add(gridHelper);
  
  console.log(' 使用备用场景');
};

// 初始化场景
const initScene = () => {
  if (!containerRef.value) return;
  
  const width = containerRef.value.clientWidth;
  const height = containerRef.value.clientHeight || 500;

  // 场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf0f4f8);

  // 相机
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(8, 6, 8);
  camera.lookAt(0, 0, 0);

  // 渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  containerRef.value.appendChild(renderer.domElement);

  // 控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.rotateSpeed = 0.8;
  controls.zoomSpeed = 0.8;
  controls.enablePan = true;
  controls.panSpeed = 0.8;
  controls.minDistance = 2;
  controls.maxDistance = Infinity;
  controls.target.set(0, 0, 0);

  // 左键平移，右键旋转
  controls.mouseButtons = {
    LEFT: THREE.MOUSE.PAN,
    MIDDLE: THREE.MOUSE.DOLLY,
    RIGHT: THREE.MOUSE.ROTATE
  };

  // 光照
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
  directionalLight.position.set(10, 20, 10);
  directionalLight.castShadow = true;
  scene.add(directionalLight);

  const backLight = new THREE.DirectionalLight(0xffffff, 0.4);
  backLight.position.set(-5, 0, 5);
  scene.add(backLight);

  // 加载模型
  const loader = new GLTFLoader();
  loadModel(loader);

  // 开始动画
  animate();
};

// 动画循环
const animate = () => {
  animationId = requestAnimationFrame(animate);
  if (controls) controls.update();
  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
};

// 窗口自适应
const handleResize = () => {
  if (!containerRef.value || !renderer || !camera) return;
  const width = containerRef.value.clientWidth;
  const height = containerRef.value.clientHeight || 500;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
};

// 手动旋转控制（点击按钮开启/关闭自动旋转）
const toggleAutoRotate = () => {
  if (controls) {
    controls.autoRotate = !controls.autoRotate;
  }
};

// 重置视角
const resetCamera = () => {
  if (camera) {
    camera.position.set(8, 6, 8);
    camera.lookAt(0, 0, 0);
    if (controls) controls.target.set(0, 0, 0);
  }
};

// 获取自动旋转状态
const getAutoRotate = () => {
  return controls ? controls.autoRotate : false;
};

// 暴露方法给父组件
defineExpose({
  toggleAutoRotate,
  resetCamera,
  getAutoRotate
});

onMounted(() => {
  initScene();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (animationId) cancelAnimationFrame(animationId);
  if (renderer) {
    renderer.dispose();
  }
});
</script>

<style scoped>
.three-container {
  width: 100%;
  height: 100%;
  min-height: 500px;
  border-radius: 12px;
  overflow: hidden;
  background: #f0f4f8;
}
</style>