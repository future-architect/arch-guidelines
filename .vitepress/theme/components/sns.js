export function addTwitter() {
  const id = "twitter-wjs";
  if (document.getElementById(id)) {
    window.twttr.widgets.load();
  } else {
    const fjs = document.getElementsByTagName("script")[0];
    const p = /^http:/.test(document.location) ? "http" : "https";
    const js = document.createElement("script");
    js.id = id;
    js.src = p + "://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);
  }
}

export function addFacebook() {
  const id = "facebook-jssdk";
  if (document.getElementById(id)) {
    window.FB.XFBML.parse();
  } else {
    const fjs = document.getElementsByTagName("script")[0];
    const p = /^http:/.test(document.location) ? "http" : "https";
    const js = document.createElement("script");
    js.id = id;
    js.src = p + "://connect.facebook.net/ja_JP/sdk.js#xfbml=1&version=v3.2";
    fjs.parentNode.insertBefore(js, fjs);
  }
}

export function addHatenaBookmark() {
  const id = "hatena-buttons";
  if (document.getElementById(id)) {
    return;
  }
  const fjs = document.getElementsByTagName("script")[0];
  const p = /^http:/.test(document.location) ? "http" : "https";
  const js = document.createElement("script");
  js.id = id;
  js.src = p + "://b.st-hatena.com/js/bookmark_button.js";
  fjs.parentNode.insertBefore(js, fjs);
}

export function addPocket(p) {
  const id = "pocket-btn-js" + p;
  // if (document.getElementById(id)) {
  // cannot reload?
  // }
  const j = document.createElement("script");
  j.id = id;
  j.src = "https://widgets.getpocket.com/v1/j/btn.js?v=1";
  document.body.appendChild(j);
}
