(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[0],{215:function(e,t,a){e.exports=a(370)},220:function(e,t,a){},221:function(e,t,a){},224:function(e,t,a){},366:function(e,t,a){},370:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),l=a(54),o=a.n(l),c=(a(220),a(221),a(222),a(223),a(38)),i=a(48),s=a(21),u=a(22),m=a(23),d=a(24),p=a(25),h=a(386),v=a(378);a(224);var g=function(e){return r.a.createElement(n.Fragment,null,r.a.createElement(c.b,{to:"/"},r.a.createElement("div",null,r.a.createElement("h2",null,e.title))))},E=a(29),b=a.n(E),y=a(34),f=a.n(y),C=a(384),S=a(92),w=a.n(S),k=(w()(),function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(m.a)(this,Object(d.a)(t).call(this,e))).background={Low:"#000000",Medium:"#FFCC00",High:"#CC0000"},a.apiServer="https://socnet.pythonanywhere.com/",a.renderTableData=function(e){return e.map((function(e){var t=e[0],n=e[1],l=e[4],o=e[6],c=e[7],i=a.background;return r.a.createElement(C.a.Row,{onClick:function(){a.props.history.push("/thread/".concat(t))}},r.a.createElement(C.a.Cell,null," Active "),r.a.createElement(C.a.Cell,{style:{color:i[e[8]]}}," ",o," "),r.a.createElement(C.a.Cell,null," ",c," "),r.a.createElement(C.a.Cell,null," ",l," "),r.a.createElement(C.a.Cell,{textAlign:"right"}," ",n," "))}))},a.state={loadingData:!1,alerts:[]},a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"componentDidMount",value:function(){return b.a.async((function(e){for(;;)switch(e.prev=e.next){case 0:try{this.setState({loadingData:!0}),console.log("ThreadAlerts.js/ComponentDidMount Props: ",this.props.location.state),this.setState({loadingData:!1,alerts:this.props.location.state.alerts})}catch(t){console.log("Error! ",t," Alerts State: ",this.state.alerts)}case 1:case"end":return e.stop()}}),null,this)}},{key:"render",value:function(){var e=this.state,t=e.loadingData,a=e.alerts;return console.log(a),t?r.a.createElement(h.a,{active:!0,inverted:!0},r.a.createElement(v.a,{size:"massive"}," Loading: fetching alerts..")):r.a.createElement("div",{style:{padding:"2%"}},r.a.createElement(C.a,{fixed:!0,singleLine:!0,padded:!0,selectable:!0,color:"teal"},r.a.createElement(C.a.Header,null,r.a.createElement(C.a.HeaderCell,null," Status "),r.a.createElement(C.a.HeaderCell,null," Type "),r.a.createElement(C.a.HeaderCell,{width:6}," Description "),r.a.createElement(C.a.HeaderCell,null," Region "),r.a.createElement(C.a.HeaderCell,{textAlign:"right"}," Date ")),r.a.createElement(C.a.Body,null,this.renderTableData(a))))}}]),t}(n.Component)),O=Object(i.f)(k),j=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(m.a)(this,Object(d.a)(t).call(this,e))).state={loadingData:!1,alerts:[]},a.apiServer="https://socnet.pythonanywhere.com/",a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"render",value:function(){var e=this.state,t=e.loadingData;e.alerts;return t?r.a.createElement(h.a,{active:!0,inverted:!0},r.a.createElement(v.a,{size:"massive"},"Loading")):r.a.createElement("div",{className:"container"},r.a.createElement(g,{title:"Socnet"}),r.a.createElement(c.b,{to:"/createAlert"},r.a.createElement("button",{type:"button",className:"btn btn-primary"},"Create Alert"))," ",r.a.createElement("br",null)," ",r.a.createElement("br",null),r.a.createElement(c.b,{to:"/"},r.a.createElement("button",{type:"button",className:"btn btn-primary"},"Filter Results")),r.a.createElement(O,null))}}]),t}(n.Component),D=a(41),x=a(382),L=a(388),N=a(379),A=a(187);var F=function(e){e.label;var t=e.type,a=e.placeholder,n=e.propChanged,l=e.values,o=e.errorMessage;return"undefined"!==typeof l?r.a.createElement(N.a,{className:"mb-3"},r.a.createElement(A.a,{placeholder:a,as:t,onChange:n,required:!0},r.a.createElement("option",{key:"Choose..."},"Choose..."),l.map((function(e){return r.a.createElement("option",{key:e},e)}))),r.a.createElement("div",null,o)):r.a.createElement(N.a,{className:"mb-3"},r.a.createElement(A.a,{placeholder:a,type:t,onChange:n,required:!0}))},T=a(126),R=a.n(T),M=a(390),H=a(391),Y=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(m.a)(this,Object(d.a)(t).call(this,e))).propChanged=function(e,t){var n=a.state.properties,r=e.target.value;console.log("props changed properties ",n),n[t].value=r,a.setState({payload:n})},a.handleSubmit=function(e){var t,n;return b.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return console.log("event is ",a.inputNode),console.log("before payload",a.state.payload),e.preventDefault(),t=a.state.payload,n=a.props.history,Object.keys(t).map((function(e){"event_severity"===e&&void 0===t[e].value?t[e]="Low":t[e]=t[e].value})),t.event_datetime=R()().format("YYYY-MM-DD hh:mm:ss"),console.log("after payload",R()().format("YYYY-MM-DD hh:mm:ss")),r.prev=8,r.next=11,b.a.awrap(f.a.post("".concat(a.apiServer,"alerts"),t));case 11:n.push("/alerts"),r.next=17;break;case 14:r.prev=14,r.t0=r.catch(8),console.log(r.t0);case 17:case"end":return r.stop()}}),null,null,[[8,14]])},a.formatItem=function(e){return e=e.includes("event")?e.substring(6,e.length):"sender's name"},a.formatType=function(e,t){return"undefined"===typeof t?"datetime"===e?"datetime-local":"text":"select"},a.firstLetterUpperCase=function(e){return e[0].toUpperCase()+e.slice(1)+": "},a.state={loadingData:!1,properties:{},requiredProperties:[],payload:{}},a.apiServer="https://socnet.pythonanywhere.com/",a.handleSubmit=a.handleSubmit.bind(Object(D.a)(a)),a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"componentDidMount",value:function(){var e;return b.a.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,this.setState({loadingData:!0}),t.next=4,b.a.awrap(f.a.get("".concat(this.apiServer,"form")));case 4:e=t.sent,this.setState({properties:e.data.properties,requiredProperties:e.data.required,loadingData:!1}),t.next=11;break;case 8:t.prev=8,t.t0=t.catch(0),console.log("error");case 11:case"end":return t.stop()}}),null,this,[[0,8]])}},{key:"render",value:function(){var e=this,t=this.state,a=t.loadingData,n=t.properties,l=t.errorMessage;return a?r.a.createElement(h.a,{active:!0,inverted:!0},r.a.createElement(v.a,{size:"massive"},"Loading")):r.a.createElement("div",{className:"container"},r.a.createElement(M.a,{basic:!0,padded:!0},r.a.createElement(H.a,{as:"h1"}," Create Alerts "),r.a.createElement(H.a,null," Please help us stay safe by entering the information about the incident you wish to report.")),r.a.createElement(M.a,{padded:"very",raised:!0,color:"teal"},r.a.createElement(x.a,{className:"container-fluid mt-4",onSubmit:function(t){return e.handleSubmit(t)}},r.a.createElement("table",{align:"center",cellPadding:"5px"},r.a.createElement("tbody",null,Object.keys(n).map((function(t){if("event_datetime"!==t)return r.a.createElement("tr",null,r.a.createElement("td",null,r.a.createElement("label",null," ",e.firstLetterUpperCase(e.formatItem(t))," ")),r.a.createElement("td",null,r.a.createElement(F,{label:e.formatItem(t),type:e.formatType(n[t].type,n[t].values),placeholder:n[t].example,propChanged:function(a){return e.propChanged(a,t)},values:n[t].values,key:e.formatItem(t),errorMessage:l})))})))),r.a.createElement(L.a,{type:"submit"}," Submit Alert  "))))}}]),t}(n.Component),B=a(67),P=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(m.a)(this,Object(d.a)(t).call(this,e))).state={eventDetails:a.props.data},a.background={Low:"light",Medium:"warning",High:"danger"},a.bgcolor={Low:"#FFFFFF",Medium:"#FFCC00",High:"#CC0000"},a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"render",value:function(){var e=this.state.eventDetails,t=this.props.linkable;return r.a.createElement(B.a,{className:"m-3"},r.a.createElement(B.a.Header,{style:{background:this.bgcolor[e[8]]},as:"h5"},e[6]),r.a.createElement(B.a.Body,null,r.a.createElement(B.a.Title,null,e[7]),r.a.createElement(B.a.Text,null,"".concat(e[3],", ").concat(e[4]," ").concat(e[2],", ").concat(e[5]," at ").concat(e[1]),r.a.createElement("br",null),"Priority: ".concat(e[8]),r.a.createElement("br",null),"Author: ".concat(e[9])),t?r.a.createElement(c.b,{to:"/thread/".concat(this.props.id)},r.a.createElement("button",{type:"button",className:"btn btn-dark"},"View Thread")):null))}}]),t}(n.Component),q=a(383),J=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(m.a)(this,Object(d.a)(t).call(this,e))).propChanged=function(e){var t=e.target.value;console.log(t);var n={text:t};a.setState({payload:n})},a.handleSubmit=function(e){var t,n;return b.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e.preventDefault(),t=a.state.payload,r.prev=2,a.setState({loadingData:!0}),console.log("".concat(a.apiServer,"threads/").concat(a.props.match.params.id)),r.next=7,b.a.awrap(f.a.put("".concat(a.apiServer,"threads/").concat(a.props.match.params.id),t));case 7:return n=r.sent,r.next=10,b.a.awrap(f.a.get("".concat(a.apiServer,"threads/").concat(a.props.match.params.id)));case 10:n=r.sent,a.setState({comments:n.data,loadingData:!1}),r.next=17;break;case 14:r.prev=14,r.t0=r.catch(2),console.log(r.t0);case 17:case"end":return r.stop()}}),null,null,[[2,14]])},a.state={loadingData:!1,comments:[],alert:[]},a.apiServer="https://socnet.pythonanywhere.com/",a.handleSubmit=a.handleSubmit.bind(Object(D.a)(a)),a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"componentDidMount",value:function(){var e,t;return b.a.async((function(a){for(;;)switch(a.prev=a.next){case 0:return a.prev=0,this.setState({loadingData:!0}),console.log(this.props),a.next=5,b.a.awrap(f.a.get("".concat(this.apiServer,"threads/").concat(this.props.match.params.id)));case 5:return e=a.sent,a.next=8,b.a.awrap(f.a.get("".concat(this.apiServer,"alerts/").concat(this.props.match.params.id)));case 8:t=a.sent,this.setState({comments:e.data,loadingData:!1,alert:t.data[0]}),console.log(this.state.comments),a.next=16;break;case 13:a.prev=13,a.t0=a.catch(0),console.log("error");case 16:case"end":return a.stop()}}),null,this,[[0,13]])}},{key:"render",value:function(){var e=this,t=this.state,a=t.loadingData,n=t.comments,l=t.alert;return a?r.a.createElement(h.a,{active:!0,inverted:!0},r.a.createElement(v.a,{size:"massive"},"Loading")):r.a.createElement("div",{className:"container"},r.a.createElement("div",{class:"col-auto"},r.a.createElement(g,{title:"Socnet"})),r.a.createElement(P,{data:l,id:l[0]}),r.a.createElement(q.a,null,n.map((function(e,t){return r.a.createElement(q.a.Item,{key:t},e[Object.keys(e)[0]])}))),r.a.createElement(N.a,null,r.a.createElement(N.a.Prepend,null,r.a.createElement(N.a.Text,null,"Add a comment")),r.a.createElement(A.a,{onChange:this.propChanged,as:"textarea","aria-label":"Add a comment"}),r.a.createElement(L.a,{variant:"dark",type:"submit",onClick:function(t){return e.handleSubmit(t)}},"Submit Comment")))}}]),t}(n.Component),U=a(39),I=a(392),z=a(381),V=a(387),_=a(66),W=a(380),G=a(385),K=function(e){function t(){var e,a;Object(s.a)(this,t);for(var n=arguments.length,r=new Array(n),l=0;l<n;l++)r[l]=arguments[l];return(a=Object(m.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(r)))).state={isFetching:!1,multiple:!0,search:!0,value:[]},a.handleChange=function(e,t){var n=t.value;a.setState({value:n}),console.log(a.state.value)},a.handleClose=function(e,t){t.value;console.log(a.state.value),console.log("Name",a.props.placeholder),a.props.handleDropdown(a.props.placeholder,a.state.value)},a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"render",value:function(){var e=this.state,t=e.isFetching,a=e.multiple,n=e.search,l=e.value;return r.a.createElement(G.a,{fluid:!0,selection:!0,disabled:t,loading:t,multiple:a,search:n,placeholder:"Select "+this.props.placeholder,options:this.props.options,noResultsMessage:"No results found.",onChange:this.handleChange,onClose:this.handleClose,selectOnNavigation:!1,value:l})}}]),t}(n.Component),$=(a(366),w()(),function(e){function t(){var e,a;Object(s.a)(this,t);for(var n=arguments.length,r=new Array(n),l=0;l<n;l++)r[l]=arguments[l];return(a=Object(m.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(r)))).state={loading:!1,date:"",severity:[],type:[],region:[]},a.apiServer="https://socnet.pythonanywhere.com/",a.severityList={name:"severity",type:"dropdown",optionList:[{key:"H",text:"High",value:"high"},{key:"L",text:"Low",value:"low"},{key:"M",text:"Medium",value:"medium"}]},a.regionList={name:"region",type:"dropdown",optionList:[{key:"NY",text:"NY - New York",value:"NY"},{key:"NJ",text:"NJ - New Jersey",value:"NJ"},{key:"CT",text:"CT - Conneticut",value:"CT"}]},a.typeList={name:"type",type:"dropdown",optionList:[{key:"Fire",text:"Fire",value:"Fire"},{key:"Earthquake",text:"Earthquake",value:"Earthquake"},{key:"Ransomware",text:"Ransomware",value:"Ransomware"}]},a.handleDropdown=function(e,t){a.setState(Object(U.a)({},e,t),(function(){console.log(e,t),console.log("Data changed by dropdown"),console.log(a.state.severity)}))},a.handleBack=function(){a.props.history.push("/main")},a.handleChange=function(e,t){var n=t.name,r=t.value;a.setState(Object(U.a)({},n,r))},a.handleValidation=function(e){return!!(e.date||e.severity.length>0||e.type.length>0||e.region.length>0)&&(console.log("User chose a filter!"),!0)},a.handleSubmit=function(e){e.preventDefault();var t=a.state,n=(t.loading,t.date),r=t.severity,l=t.type,o=t.region,c=(a.apiServer,{date:n,severity:r,type:l,region:o});if(a.handleValidation(c)){console.log("Form had entries: ",JSON.stringify(c),typeof c);try{f.a.get("".concat(a.apiServer,"alerts")).then((function(e){a.setState({loading:!1}),a.props.history.push("/alerts",{alerts:e.data})}))}catch(e){console.log("ERROR: UNABLE TO FETCH FILTERED RESULTS")}}else{console.log("The form had no entries. Attempting to load all alerts.");try{f.a.get("".concat(a.apiServer,"alerts")).then((function(e){a.setState({loading:!1}),console.log("Alerts loaded. Payload looks like: ",e.data),a.props.history.push("/alerts",{alerts:e.data})}))}catch(e){console.log("ERROR: UNABLE TO GET ALL RESULTS.")}}},a}return Object(p.a)(t,e),Object(u.a)(t,[{key:"render",value:function(){var e=this,t=this.state,a=t.loading,n=t.severity,l=t.date,o=t.region,c=t.type;return a?r.a.createElement(h.a,{active:!0,inverted:!0},r.a.createElement(v.a,{size:"massive"}," Loading: fetching alerts..")):r.a.createElement("div",null,r.a.createElement(M.a,{basic:!0,padded:!0}," ",r.a.createElement(H.a,{as:"h1"}," Filter Alerts ")," "),r.a.createElement(M.a,{padded:"very",raised:!0,color:"teal"},r.a.createElement(I.a,{centered:!0},r.a.createElement(z.a,{loading:a,onSubmit:this.handleSubmit.bind(this),size:"large",style:{width:"60%"}},r.a.createElement("table",{align:"center",className:"filters",cellPadding:"5px"},r.a.createElement("tbody",null,r.a.createElement("tr",null,r.a.createElement("td",null," ",r.a.createElement("label",null," Since (Date): "),"  "),r.a.createElement("td",null,r.a.createElement("input",{type:"date",placeholder:"mm/dd/yyyy",onChange:function(t){return e.setState({date:t.target.value})}}))),r.a.createElement("tr",null,r.a.createElement("td",null," ",r.a.createElement("label",null," Severity: ")," "),r.a.createElement("td",null,r.a.createElement(K,{placeholder:this.severityList.name,options:this.severityList.optionList,handleDropdown:this.handleDropdown}))),r.a.createElement("tr",null,r.a.createElement("td",null," ",r.a.createElement("label",null," Type: ")," "),r.a.createElement("td",null,r.a.createElement(K,{placeholder:this.typeList.name,options:this.typeList.optionList,handleDropdown:this.handleDropdown}))),r.a.createElement("tr",null,r.a.createElement("td",null," ",r.a.createElement("label",null," Region: ")),r.a.createElement("td",null,r.a.createElement(K,{placeholder:this.regionList.name,options:this.regionList.optionList,handleDropdown:this.handleDropdown}))))),r.a.createElement("br",null),r.a.createElement(V.a,{animated:!0,onClick:function(t){return e.handleBack.bind(e)}},r.a.createElement(V.a.Content,{visible:!0}," Back "),r.a.createElement(V.a.Content,{hidden:!0},r.a.createElement(_.a,{name:"arrow left"}))),r.a.createElement(V.a,{type:"submit",animated:!0},r.a.createElement(V.a.Content,{visible:!0},"Submit"),r.a.createElement(V.a.Content,{hidden:!0},r.a.createElement(_.a,{name:"arrow right"})))))),r.a.createElement("br",null),r.a.createElement("strong",null," LEAVE BLANK FOR ALL "),r.a.createElement(W.a,null),r.a.createElement("strong",null," For testing before backend integration "),r.a.createElement("pre",null,JSON.stringify({severity:n,date:l,region:o,type:c})))}}]),t}(n.Component)),Q=Object(i.f)($);var X=function(){return r.a.createElement("div",{className:"App"},r.a.createElement(c.a,{basename:"/socnet/webapp.html#"},r.a.createElement(i.c,null,r.a.createElement(i.a,{exact:!0,path:"/",component:Q}),r.a.createElement(i.a,{exact:!0,path:"/alerts",component:j}),r.a.createElement(i.a,{exact:!0,path:"/createAlert",component:Y}),r.a.createElement(i.a,{exact:!0,path:"/thread/:id",component:J}))))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));o.a.render(r.a.createElement(X,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[215,1,2]]]);
//# sourceMappingURL=main.d8e70f1b.chunk.js.map