import{d as r,V as a,a5 as o,a6 as n,a7 as h}from"./framework.9KRWhLjn.js";const l=r({name:"github-button",props:{href:String,ariaLabel:String,title:String,dataIcon:String,dataColorScheme:String,dataSize:String,dataShowCount:String,dataText:String},render:function(){const t={ref:"_"};for(const e in this.$props)t[o(e)]=this.$props[e];return n("span",[h(this.$slots,"default")?n("a",t,this.$slots.default()):n("a",t)])},mounted:function(){this.paint()},beforeUpdate:function(){this.reset()},updated:function(){this.paint()},beforeUnmount:function(){this.reset()},methods:{paint:function(){if(this.$el.lastChild!==this.$refs._)return;const t=this.$el.appendChild(document.createElement("span")),e=this;a(()=>import("./buttons.esm.DK2fWHEW.js"),[]).then(function(i){e.$el.lastChild===t&&i.render(t.appendChild(e.$refs._),function(s){e.$el.lastChild===t&&t.parentNode.replaceChild(s,t)})})},reset:function(){this.$refs._!=null&&this.$el.replaceChild(this.$refs._,this.$el.lastChild)}}});export{l as default};
