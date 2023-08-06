import { defineComponent, openBlock, createElementBlock, Fragment, createElementVNode } from "../vue.esm-browser.prod.js";
import katex from "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.mjs";
const _hoisted_1 = /* @__PURE__ */ createElementVNode("link", {
  rel: "stylesheet",
  href: "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css",
  integrity: "sha384-Xi8rHCmBmhbuyyhbI88391ZKP2dmfnOl4rT9ZfRI7mLTdk1wblIUnrIq35nqwEvC",
  crossorigin: "anonymous"
}, null, -1);
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "Formula",
  props: {
    content: null
  },
  setup(__props) {
    const p = __props;
    const renderFormula = (node) => {
      try {
        katex.render(p.content, node);
      } catch (e) {
        console.error(`Error rendering formula: ${e}`);
      }
    };
    const formulaRef = (node) => {
      if (node) {
        renderFormula(node);
      }
    };
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock(Fragment, null, [
        _hoisted_1,
        createElementVNode("div", {
          "data-cy": "block-formula",
          className: "w-full overflow-y-hidden bg-white flex justify-center",
          ref: formulaRef
        })
      ], 64);
    };
  }
});
export { _sfc_main as default };
