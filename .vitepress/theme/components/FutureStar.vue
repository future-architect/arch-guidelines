<template>
  <div class="future-star__container" :class="['future-star--kind-' + kind]">
    <div class="future-star"></div>
  </div>
</template>

<script setup>
const { kind } = defineProps({ kind: { type: String, required: true } });
const starSize = 10;
const lengthRate = 32; /* 正確には22程度だが動いていると短く見えるので長めに設定する */
const starWidth = starSize * (lengthRate + 0.5);
const starPath = `path("M 0 ${starSize / 2} l ${starSize * lengthRate} -${starSize / 2} a 1 1 0 0 1 0 ${starSize} Z")`;
</script>

<style scoped>
:global(.standards-home .clip) {
  /* タイトルをアンカーにする */
  anchor-name: --future-title;
}

.future-star__container {
  position: fixed;
  width: calc(100vw + v-bind(starWidth * 2 + "px"));
  min-width: calc(800px + v-bind(starWidth * 2 + "px"));
  bottom: calc(100vh - 160px); /* fallback */
  z-index: -1; /* fallback の場合にコンテンツの後ろに配置したいので-1 */
  position-anchor: --future-title;
  bottom: calc(anchor(top) - 10px);
  left: v-bind(-starWidth + "px");
  filter: blur(3px);
  transform-origin: left 50%;
  opacity: 0.1;
}
.dark .future-star__container {
  opacity: 0.2;
}
.future-star--kind-1 {
  transform: rotate(-6deg);
}
.future-star--kind-2 {
  transform: rotate(-4deg);
}
.future-star {
  position: absolute;
  background-color: #da0058;
  height: v-bind(starSize + "px");
  width: v-bind(starWidth + "px");
  clip-path: v-bind(starPath);

  animation-composition: add;
  animation-name: slide-to-right;
  animation-duration: 10s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}
.future-star--kind-2 .future-star {
  animation-delay: 250ms;
}
@keyframes slide-to-right {
  0% {
    left: 0;
  }
  50% {
    left: 100%;
  }
  100% {
    left: 100%;
  }
}
</style>
