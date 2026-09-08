<template>
  <div class="vitepress-page-title">
    <ul class="share-buttons" aria-label="共有">
      <li v-for="s in shares" :key="s.label" class="share-item">
        <a
          class="share-btn"
          :href="s.href"
          target="_blank"
          rel="noopener"
          :title="s.label"
          :aria-label="s.label"
        >
          <svg
            class="share-btn-icon"
            :viewBox="s.icon.viewBox"
            fill="currentColor"
            aria-hidden="true"
          >
            <path v-for="d in s.icon.paths" :key="d" :d="d" />
          </svg>
        </a>
      </li>
      <li v-if="canCopy" class="share-item">
        <button
          type="button"
          class="share-btn"
          :class="{ 'is-copied': copied }"
          :title="copyLabel"
          @click="copyLink"
        >
          <svg
            class="share-btn-icon share-btn-icon--line"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path v-for="d in LINK_ICON" :key="d" :d="d" />
          </svg>
          <svg
            class="share-btn-icon share-btn-icon--line share-icon-done"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M5 12l5 5l10 -10" />
          </svg>
          <span class="visually-hidden" aria-live="polite">{{
            copyLabel
          }}</span>
        </button>
        <span class="share-copied" aria-hidden="true">コピーしました</span>
      </li>
    </ul>

    <h1 class="vitepress-page-title__title">
      {{ page.title }}
    </h1>
    <div class="vitepress-page-title__author">
      {{ page.frontmatter.author }}
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useData, useRoute } from "vitepress";

/**
 * `markdown-it-plugin-header-shift`でheaderタグを1つづつずらす前提であるため、Markdownファイルにはタイトルがありません。
 * これを回避するためにMarkdownファイルの先頭に`<page-title/>`を記述させることでタイトルを表示させます。
 *
 * 共有ボタンは技術ブログ（future-architect.github.io）と同じ形。intent URL への素のリンクで、
 * 各サービスの SDK は読まない。ロゴは塗りのインライン SVG で、色は currentColor で追従させる。
 */
const { page, site } = useData();
const route = useRoute();

const pageUrl = computed(
  () => "https://future-architect.github.io" + route.path,
);

const ICONS = {
  x: {
    viewBox: "0 0 1200 1227",
    paths: [
      "M714.163 519.284L1160.89 0H1055.03L667.137 450.887L357.328 0H0L468.492 681.821L0 1226.37h105.866L515.491 750.218L842.672 1226.37H1200L714.137 519.284H714.163ZM658.88 583.579L569.165 687.828L892.476 1150.301H1055.08L658.88 583.579ZM611.412 515.685L306.615 79.6944H144.011L521.697 619.934L611.412 515.685Z",
    ],
  },
  facebook: {
    viewBox: "0 0 12.8 24",
    paths: [
      "M8.308,24V13.053h3.774l.565-4.266H8.308V6.061c0-1.235.352-2.077,2.171-2.077h2.32V.168A31.887,31.887,0,0,0,9.418,0C6.073,0,3.783,1.988,3.783,5.64V8.786H0v4.266H3.783V24Z",
    ],
  },
  hatebu: {
    viewBox: "0 0 355.004 300",
    paths: [
      "M280.009,0h70v200.005h-70V0z",
      "M215.192,160.596c-11.844-13.239-28.314-20.683-49.443-22.288c18.795-5.122,32.443-12.616,41.077-22.628c8.593-9.88,12.856-23.292,12.856-40.171c0-13.362-2.922-25.184-8.579-35.397c-5.805-10.152-14.14-18.276-25.102-24.357c-9.586-5.274-20.98-8.994-34.262-11.188c-13.349-2.126-36.709-3.198-70.231-3.198H0V298.63h83.976c33.737,0,58.064-1.182,72.94-3.441c14.863-2.337,27.334-6.27,37.428-11.662c12.484-6.587,22.007-15.964,28.662-28.01c6.698-12.085,10.014-26.02,10.014-41.956C233.017,191.514,227.079,173.798,215.192,160.596z M75.26,67.27h17.398c20.108,0,33.617,2.267,40.59,6.787c6.877,4.542,10.388,12.38,10.388,23.547c0,10.745-3.733,18.313-11.118,22.751c-7.483,4.354-21.117,6.562-41.079,6.562H75.26V67.27z M144.276,237.733c-7.916,4.862-21.557,7.251-40.696,7.251H75.265v-64.949h29.54c19.654,0,33.243,2.475,40.469,7.414c7.343,4.942,10.955,13.665,10.955,26.191C156.226,224.85,152.263,232.899,144.276,237.733z",
      "M315.014,220.003c-22.101,0-40.002,17.891-40.002,39.991c0,22.1,17.902,40.006,40.002,40.006c22.072,0,39.99-17.906,39.99-40.006C355.004,237.894,337.088,220.003,315.014,220.003z",
    ],
  },
};

// Tabler Icons（MIT / https://tabler.io/icons ）の link
const LINK_ICON = [
  "M9 15l6 -6",
  "M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464",
  "M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463",
];

const shares = computed(() => {
  const url = pageUrl.value;
  const text = `${page.value.title} | ${site.value.title}`;
  return [
    {
      icon: ICONS.x,
      label: "Xでポストする",
      href: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`,
    },
    {
      icon: ICONS.facebook,
      label: "Facebookでシェアする",
      href: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
    },
    {
      // リンク先は追加フォームではなくエントリーページなので「見る」
      icon: ICONS.hatebu,
      label: "はてなブックマークで見る",
      href: `https://b.hatena.ne.jp/entry/s/${encodeURI(url).replace("https://", "")}`,
    },
  ];
});

// クリップボードへの書き込みは https（と localhost）でしか許可されないので、
// 押しても何も起きないボタンを見せない
const canCopy = ref(false);
const copied = ref(false);
const copyLabel = computed(() =>
  copied.value ? "リンクをコピーしました" : "リンクをコピーする",
);
let copiedTimer;

onMounted(() => {
  canCopy.value = Boolean(navigator.clipboard) && window.isSecureContext;
});

function copyLink() {
  navigator.clipboard.writeText(pageUrl.value).then(() => {
    copied.value = true;
    clearTimeout(copiedTimer);
    copiedTimer = setTimeout(() => {
      copied.value = false;
    }, 2000);
  });
}
</script>

<style scoped>
/* .vp-doc の ul / li / a の既定（字下げ・行間・下線・青）を打ち消す */
.share-buttons {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.share-item {
  margin: 0;
  position: relative;
}
.share-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  box-sizing: border-box;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: transparent;
  color: var(--vp-c-brand-3);
  text-decoration: none;
  font: inherit;
  cursor: pointer;
  transition:
    background-color 0.05s ease,
    border-color 0.05s ease,
    color 0.05s ease;
}
.share-btn:hover,
.share-btn:focus-visible {
  background: var(--vp-c-brand-3);
  border-color: var(--vp-c-brand-3);
  color: #fff;
  text-decoration: none;
}
/* ダークではネイビーが地に沈むので、明るい青で置く */
.dark .share-btn {
  color: var(--vp-c-brand-1);
}
.dark .share-btn:hover,
.dark .share-btn:focus-visible {
  background: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
}
.share-btn-icon {
  display: block;
  width: 14px;
  height: 14px;
}
.share-btn-icon--line {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
/* コピーの合図は2つ。円の中のアイコンをチェックに差し替え、円の上に吹き出しを出す。
   吹き出しは absolute で浮かせて、押した瞬間にボタンの並びが動かないようにする */
.share-copied {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 6px;
  padding: 3px 8px;
  border-radius: 4px;
  background: var(--vp-c-brand-3);
  color: #fff;
  font-size: 12px;
  font-weight: bold;
  line-height: 1.4;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.05s ease;
}
.dark .share-copied {
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
}
.share-btn.is-copied + .share-copied {
  opacity: 1;
}
.share-icon-done {
  display: none;
}
.share-btn.is-copied > .share-btn-icon {
  display: none;
}
.share-btn.is-copied > .share-icon-done {
  display: block;
}

.vitepress-page-title__author {
  padding-bottom: 8px;
  margin-bottom: 18px;
  font-size: 12px;
  border: none;
  color: initial;
  text-align: right;
  page-break-after: always;

  font-weight: 600;
  line-height: 1.25;

  border-bottom: 1px solid #eaecef;
}

@media print {
  .share-buttons {
    display: none;
  }

  .vitepress-page-title__title {
    text-align: center;
    margin-top: 50%;
    page-break-before: auto;
  }
  .vitepress-page-title__author {
    page-break-after: always;
  }
}
</style>
