import{_ as g,C as p,c as E,o as e,G as a,a4 as n,b as h,j as t,w as l,a as i,a8 as r}from"./chunks/framework.9KRWhLjn.js";const o="/arch-guidelines/assets/image7.Gf1GnjVN.png",y="/arch-guidelines/assets/image8.ao0Cxhtt.png",c="/arch-guidelines/assets/image9.Bf9R6IqE.png",f="/arch-guidelines/assets/image12.CmF7cC0W.jpg",C=JSON.parse('{"title":"PostgreSQL設計ガイドライン","description":"","frontmatter":{"sidebarDepth":4,"title":"PostgreSQL設計ガイドライン","author":"フューチャー株式会社","head":[["meta",{"name":"keywords","content":"Web API"}]]},"headers":[],"relativePath":"documents/forDB/postgresql_guidelines.md","filePath":"documents/forDB/postgresql_guidelines.md"}'),b={name:"documents/forDB/postgresql_guidelines.md"};function u(x,s,A,m,D,F){const k=p("page-title"),d=p("Mermaid");return e(),E("div",null,[a(k),s[3]||(s[3]=n("",548)),(e(),h(r,null,{default:l(()=>[a(d,{id:"mermaid-6367",class:"mermaid",graph:"sequenceDiagram%0A%20%20%20%20participant%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC1%0A%20%20%20%20participant%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC2%0A%20%20%20%20participant%20WebApp%0A%20%20%20%20participant%20DB%0A%0A%0A%20%20%20%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC1%20-%3E%3E%20WebApp%3A%20%E5%9C%A8%E5%BA%AB%E5%BC%95%E5%BD%93%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%20(-5)%0A%20%20%20%20WebApp%20-%3E%3E%20DB%3A%20UPDATE%20%E5%9C%A8%E5%BA%AB%20SET%20%E6%95%B0%E9%87%8F%20%3D%20%E6%95%B0%E9%87%8F%20-%205%20WHERE%20%E5%95%86%E5%93%81ID%20%3D%201%20AND%20%E6%95%B0%E9%87%8F%20%3E%3D%205%0A%20%20%20%20DB%20--%3E%3E%20WebApp%3A%20%E6%9B%B4%E6%96%B0%E6%88%90%E5%8A%9F%EF%BC%88%E6%9B%B4%E6%96%B0%E4%BB%B6%E6%95%B0%201%EF%BC%89%0A%20%20%20%20WebApp%20--%3E%3E%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC1%3A%20%E5%BC%95%E5%BD%93%E6%88%90%E5%8A%9F%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E8%A1%A8%E7%A4%BA%0A%0A%0A%20%20%20%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC2%20-%3E%3E%20WebApp%3A%20%E5%9C%A8%E5%BA%AB%E5%BC%95%E5%BD%93%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%20(-10)%0A%20%20%20%20WebApp%20-%3E%3E%20DB%3A%20UPDATE%20%E5%9C%A8%E5%BA%AB%20SET%20%E6%95%B0%E9%87%8F%20%3D%20%E6%95%B0%E9%87%8F%20-%2010%20WHERE%20%E5%95%86%E5%93%81ID%20%3D%201%20AND%20%E6%95%B0%E9%87%8F%20%3E%3D%2010%0A%20%20%20%20DB%20--%3E%3E%20WebApp%3A%20%E6%9B%B4%E6%96%B0%E5%A4%B1%E6%95%97%EF%BC%88%E6%9B%B4%E6%96%B0%E4%BB%B6%E6%95%B0%200%EF%BC%89%0A%20%20%20%20WebApp%20--%3E%3E%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC2%3A%20%E5%9C%A8%E5%BA%AB%E4%B8%8D%E8%B6%B3%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E8%A1%A8%E7%A4%BA%0A"})]),fallback:l(()=>s[0]||(s[0]=[i(" Loading... ")])),_:1})),s[4]||(s[4]=n("",215)),(e(),h(r,null,{default:l(()=>[a(d,{id:"mermaid-9248",class:"mermaid",graph:"sequenceDiagram%0A%20%20%20%20participant%20User%20as%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%0A%20%20%20%20participant%20App%20as%20%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%0A%20%20%20%20participant%20DB%20as%20PostgreSQL%0A%20%20%20%20participant%20SearchEngine%20as%20%E5%85%A8%E6%96%87%E6%A4%9C%E7%B4%A2%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%B3%0A%0A%20%20%20%20User-%3E%3EApp%3A%20%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%0A%20%20%20%20App-%3E%3EApp%3A%20%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B6%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E9%96%8B%E5%A7%8B%0A%20%20%20%20App-%3E%3EDB%3A%20%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%81%BF%0A%20%20%20%20App-%3E%3ESearchEngine%3A%20%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%81%BF%0A%20%20%20%20App-%3E%3EApp%3A%20%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%0A%20%20%20%20App-%3E%3EUser%3A%20%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%E6%88%90%E5%8A%9F%0A"})]),fallback:l(()=>s[1]||(s[1]=[i(" Loading... ")])),_:1})),s[5]||(s[5]=t("h4",{id:"_2-非同期",tabindex:"-1"},[i("2. 非同期 "),t("a",{class:"header-anchor",href:"#_2-非同期","aria-label":'Permalink to "2. 非同期"'},"​")],-1)),s[6]||(s[6]=t("p",null,[i("通常、全文検索エンジンはデータ登録が高速であるため、「1.同期」の全文検索において、キューイングシステム（例えばAWS SQS）を経由する意味があまりない。追加でRedisが必要となるが、PostgreSQLの"),t("a",{href:"https://www.postgresql.org/docs/current/logicaldecoding.html",target:"_blank",rel:"noreferrer"},"論理レコード"),i("を利用した、PGSyncを利用した構成案も考えられる。")],-1)),(e(),h(r,null,{default:l(()=>[a(d,{id:"mermaid-9255",class:"mermaid",graph:"sequenceDiagram%0A%20%20%20%20participant%20User%20as%20%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%0A%20%20%20%20participant%20App%20as%20%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%0A%20%20%20%20participant%20DB%20as%20PostgreSQL%0A%20%20%20%20participant%20PGSync%20as%20PGSync%0A%20%20%20%20participant%20SearchEngine%20as%20%E5%85%A8%E6%96%87%E6%A4%9C%E7%B4%A2%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%B3%0A%0A%20%20%20%20User-%3E%3EApp%3A%20%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%0A%20%20%20%20App-%3E%3EDB%3A%20%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%81%BF%0A%20%20%20%20App-%3E%3EApp%3A%20%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%0A%20%20%20%20App-%3E%3EUser%3A%20%E3%82%A2%E3%83%83%E3%83%97%E3%83%AD%E3%83%BC%E3%83%89%E6%88%90%E5%8A%9F%0A%20%20%20%20PGSync-%3E%3EDB%3A%20%E8%AB%96%E7%90%86%E3%83%87%E3%82%B3%E3%83%BC%E3%83%89%E3%81%A7%E5%A4%89%E6%9B%B4%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3%E3%82%92%E5%8F%96%E5%BE%97%0A%20%20%20%20PGSync-%3E%3ESearchEngine%3A%20%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%81%BF%0A"})]),fallback:l(()=>s[2]||(s[2]=[i(" Loading... ")])),_:1})),s[7]||(s[7]=n("",85)),s[8]||(s[8]=t("table",{tabindex:"0"},[t("thead",null,[t("tr",null,[t("th",{style:{"text-align":"left"}},"案"),t("th",{style:{"text-align":"left"}},"説明"),t("th",{style:{"text-align":"left"}},"判例")])]),t("tbody",null,[t("tr",null,[t("td",{style:{"text-align":"left"}},"（1）個人単位で払い出し ※推奨"),t("td",{style:{"text-align":"left"}},"保守運用者1人ずつに払い出す方式。J-SOXに従うなど厳格に管理する必要がある場合に用いる。メンテナンスロール以上を付与する場合は、同時に読み取り専用のユーザーも作成する"),t("td",{style:{"text-align":"left"}},[i("{スキーマ}"),t("em",{会社名:""},"ope"),t("em",{会社名:""},[i("名称"),t("br"),i(" {スキーマ}_ope")]),i("_名称_readonly"),t("br"),i(" ---"),t("br"),i(" foo_ope_future_mano91"),t("br"),i(" foo_ope_future_mano91_readonly")])]),t("tr",null,[t("td",{style:{"text-align":"left"}},"（2）組織単位で払い出し ※1と組み合わせて利用"),t("td",{style:{"text-align":"left"}},"部署／会社などの組織単位で作成する。例えばメインで開発する会社と、一部外部の開発会社に依頼した場合を想定する。"),t("td",{style:{"text-align":"left"}},[i("{スキーマ}"),t("em",{会社名:""},"ope"),t("br"),i(" {スキーマ}"),t("em",{会社名:""},"ope"),i("_readonly")])]),t("tr",null,[t("td",{style:{"text-align":"left"}},"（3）アカウント共有 ※原則禁止"),t("td",{style:{"text-align":"left"}},"ロールごとに1つのユーザーを作成して共有する方式"),t("td",{style:{"text-align":"left"}},"foo_ope_maintener foo_ope_readonly")])])],-1)),s[9]||(s[9]=n("",62))])}const T=g(b,[["render",u]]);export{C as __pageData,T as default};
