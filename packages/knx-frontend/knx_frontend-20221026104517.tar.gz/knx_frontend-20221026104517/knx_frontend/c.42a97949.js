import{_ as n,s as e,e as i,t,$ as d,r as o,n as s}from"./main-f63f5335.js";import"lit-html/is-server.js";import{g as r}from"./c.53796d6b.js";let a=n([s("knx-overview")],(function(n,e){return{F:class extends e{constructor(...e){super(...e),n(this)}},d:[{kind:"field",decorators:[i({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[t()],key:"knxInfo",value:()=>null},{kind:"method",key:"firstUpdated",value:function(){r(this.hass).then(n=>{this.knxInfo=n,this.requestUpdate()})}},{kind:"method",key:"render",value:function(){var n,e,i;return this.knxInfo?d`
      <ha-card class="knx-info" header="KNX Information">
        <div class="card-content knx-info-section">
          <div class="knx-content-row">
            <div>XKNX Version</div>
            <div>${null===(n=this.knxInfo)||void 0===n?void 0:n.version}</div>
          </div>

          <div class="knx-content-row">
            <div>Connected to Bus</div>
            <div>${null!==(e=this.knxInfo)&&void 0!==e&&e.connected?"Yes":"No"}</div>
          </div>

          <div class="knx-content-row">
            <div>Individual address</div>
            <div>${null===(i=this.knxInfo)||void 0===i?void 0:i.current_address}</div>
          </div>
        </div>
      </ha-card>
    `:d`Loading...`}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      .knx-info {
        max-width: 400px;
      }

      .knx-info-section {
        display: flex;
        flex-direction: column;
      }

      .knx-content-row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }
    `}}]}}),e);export{a as KNXOverview};
