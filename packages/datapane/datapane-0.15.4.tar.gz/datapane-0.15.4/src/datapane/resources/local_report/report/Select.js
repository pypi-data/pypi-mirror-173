import { openBlock, createBlock, withKeys, withModifiers, renderSlot, createVNode, withDirectives, Fragment, renderList, toDisplayString, vShow, createCommentVNode, Transition, withCtx, createTextVNode, defineComponent, ref, computed, createElementBlock, createElementVNode, normalizeClass, unref } from "../vue.esm-browser.prod.js";
function isEmpty(opt) {
  if (opt === 0)
    return false;
  if (Array.isArray(opt) && opt.length === 0)
    return true;
  return !opt;
}
function not(fun) {
  return (...params) => !fun(...params);
}
function includes(str, query) {
  if (str === void 0)
    str = "undefined";
  if (str === null)
    str = "null";
  if (str === false)
    str = "false";
  const text = str.toString().toLowerCase();
  return text.indexOf(query.trim()) !== -1;
}
function filterOptions(options, search, label, customLabel) {
  return search ? options.filter((option) => includes(customLabel(option, label), search)).sort((a, b) => customLabel(a, label).length - customLabel(b, label).length) : options;
}
function stripGroups(options) {
  return options.filter((option) => !option.$isLabel);
}
function flattenOptions(values, label) {
  return (options) => options.reduce((prev, curr) => {
    if (curr[values] && curr[values].length) {
      prev.push({
        $groupLabel: curr[label],
        $isLabel: true
      });
      return prev.concat(curr[values]);
    }
    return prev;
  }, []);
}
function filterGroups(search, label, values, groupLabel, customLabel) {
  return (groups) => groups.map((group) => {
    if (!group[values]) {
      console.warn(`Options passed to vue-multiselect do not contain groups, despite the config.`);
      return [];
    }
    const groupOptions = filterOptions(group[values], search, label, customLabel);
    return groupOptions.length ? {
      [groupLabel]: group[groupLabel],
      [values]: groupOptions
    } : [];
  });
}
const flow = (...fns) => (x) => fns.reduce((v, f) => f(v), x);
var multiselectMixin = {
  data() {
    return {
      search: "",
      isOpen: false,
      preferredOpenDirection: "below",
      optimizedHeight: this.maxHeight
    };
  },
  props: {
    internalSearch: {
      type: Boolean,
      default: true
    },
    options: {
      type: Array,
      required: true
    },
    multiple: {
      type: Boolean,
      default: false
    },
    trackBy: {
      type: String
    },
    label: {
      type: String
    },
    searchable: {
      type: Boolean,
      default: true
    },
    clearOnSelect: {
      type: Boolean,
      default: true
    },
    hideSelected: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: "Select option"
    },
    allowEmpty: {
      type: Boolean,
      default: true
    },
    resetAfter: {
      type: Boolean,
      default: false
    },
    closeOnSelect: {
      type: Boolean,
      default: true
    },
    customLabel: {
      type: Function,
      default(option, label) {
        if (isEmpty(option))
          return "";
        return label ? option[label] : option;
      }
    },
    taggable: {
      type: Boolean,
      default: false
    },
    tagPlaceholder: {
      type: String,
      default: "Press enter to create a tag"
    },
    tagPosition: {
      type: String,
      default: "top"
    },
    max: {
      type: [Number, Boolean],
      default: false
    },
    id: {
      default: null
    },
    optionsLimit: {
      type: Number,
      default: 1e3
    },
    groupValues: {
      type: String
    },
    groupLabel: {
      type: String
    },
    groupSelect: {
      type: Boolean,
      default: false
    },
    blockKeys: {
      type: Array,
      default() {
        return [];
      }
    },
    preserveSearch: {
      type: Boolean,
      default: false
    },
    preselectFirst: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    if (!this.multiple && this.max) {
      console.warn("[Vue-Multiselect warn]: Max prop should not be used when prop Multiple equals false.");
    }
    if (this.preselectFirst && !this.internalValue.length && this.options.length) {
      this.select(this.filteredOptions[0]);
    }
  },
  computed: {
    internalValue() {
      return this.modelValue || this.modelValue === 0 ? Array.isArray(this.modelValue) ? this.modelValue : [this.modelValue] : [];
    },
    filteredOptions() {
      const search = this.search || "";
      const normalizedSearch = search.toLowerCase().trim();
      let options = this.options.concat();
      if (this.internalSearch) {
        options = this.groupValues ? this.filterAndFlat(options, normalizedSearch, this.label) : filterOptions(options, normalizedSearch, this.label, this.customLabel);
      } else {
        options = this.groupValues ? flattenOptions(this.groupValues, this.groupLabel)(options) : options;
      }
      options = this.hideSelected ? options.filter(not(this.isSelected)) : options;
      if (this.taggable && normalizedSearch.length && !this.isExistingOption(normalizedSearch)) {
        if (this.tagPosition === "bottom") {
          options.push({ isTag: true, label: search });
        } else {
          options.unshift({ isTag: true, label: search });
        }
      }
      return options.slice(0, this.optionsLimit);
    },
    valueKeys() {
      if (this.trackBy) {
        return this.internalValue.map((element) => element[this.trackBy]);
      } else {
        return this.internalValue;
      }
    },
    optionKeys() {
      const options = this.groupValues ? this.flatAndStrip(this.options) : this.options;
      return options.map((element) => this.customLabel(element, this.label).toString().toLowerCase());
    },
    currentOptionLabel() {
      return this.multiple ? this.searchable ? "" : this.placeholder : this.internalValue.length ? this.getOptionLabel(this.internalValue[0]) : this.searchable ? "" : this.placeholder;
    }
  },
  watch: {
    internalValue() {
      if (this.resetAfter && this.internalValue.length) {
        this.search = "";
        this.$emit("update:modelValue", this.multiple ? [] : null);
      }
    },
    search() {
      this.$emit("search-change", this.search);
    }
  },
  emits: ["open", "search-change", "close", "select", "update:modelValue", "remove", "tag"],
  methods: {
    getValue() {
      return this.multiple ? this.internalValue : this.internalValue.length === 0 ? null : this.internalValue[0];
    },
    filterAndFlat(options, search, label) {
      return flow(
        filterGroups(search, label, this.groupValues, this.groupLabel, this.customLabel),
        flattenOptions(this.groupValues, this.groupLabel)
      )(options);
    },
    flatAndStrip(options) {
      return flow(
        flattenOptions(this.groupValues, this.groupLabel),
        stripGroups
      )(options);
    },
    updateSearch(query) {
      this.search = query;
    },
    isExistingOption(query) {
      return !this.options ? false : this.optionKeys.indexOf(query) > -1;
    },
    isSelected(option) {
      const opt = this.trackBy ? option[this.trackBy] : option;
      return this.valueKeys.indexOf(opt) > -1;
    },
    isOptionDisabled(option) {
      return !!option.$isDisabled;
    },
    getOptionLabel(option) {
      if (isEmpty(option))
        return "";
      if (option.isTag)
        return option.label;
      if (option.$isLabel)
        return option.$groupLabel;
      const label = this.customLabel(option, this.label);
      if (isEmpty(label))
        return "";
      return label;
    },
    select(option, key) {
      if (option.$isLabel && this.groupSelect) {
        this.selectGroup(option);
        return;
      }
      if (this.blockKeys.indexOf(key) !== -1 || this.disabled || option.$isDisabled || option.$isLabel)
        return;
      if (this.max && this.multiple && this.internalValue.length === this.max)
        return;
      if (key === "Tab" && !this.pointerDirty)
        return;
      if (option.isTag) {
        this.$emit("tag", option.label, this.id);
        this.search = "";
        if (this.closeOnSelect && !this.multiple)
          this.deactivate();
      } else {
        const isSelected = this.isSelected(option);
        if (isSelected) {
          if (key !== "Tab")
            this.removeElement(option);
          return;
        }
        this.$emit("select", option, this.id);
        if (this.multiple) {
          this.$emit("update:modelValue", this.internalValue.concat([option]));
        } else {
          this.$emit("update:modelValue", option);
        }
        if (this.clearOnSelect)
          this.search = "";
      }
      if (this.closeOnSelect)
        this.deactivate();
    },
    selectGroup(selectedGroup) {
      const group = this.options.find((option) => {
        return option[this.groupLabel] === selectedGroup.$groupLabel;
      });
      if (!group)
        return;
      if (this.wholeGroupSelected(group)) {
        this.$emit("remove", group[this.groupValues], this.id);
        const newValue = this.internalValue.filter(
          (option) => group[this.groupValues].indexOf(option) === -1
        );
        this.$emit("update:modelValue", newValue);
      } else {
        const optionsToAdd = group[this.groupValues].filter(
          (option) => !(this.isOptionDisabled(option) || this.isSelected(option))
        );
        this.$emit("select", optionsToAdd, this.id);
        this.$emit(
          "update:modelValue",
          this.internalValue.concat(optionsToAdd)
        );
      }
      if (this.closeOnSelect)
        this.deactivate();
    },
    wholeGroupSelected(group) {
      return group[this.groupValues].every(
        (option) => this.isSelected(option) || this.isOptionDisabled(option)
      );
    },
    wholeGroupDisabled(group) {
      return group[this.groupValues].every(this.isOptionDisabled);
    },
    removeElement(option, shouldClose = true) {
      if (this.disabled)
        return;
      if (option.$isDisabled)
        return;
      if (!this.allowEmpty && this.internalValue.length <= 1) {
        this.deactivate();
        return;
      }
      const index = typeof option === "object" ? this.valueKeys.indexOf(option[this.trackBy]) : this.valueKeys.indexOf(option);
      this.$emit("remove", option, this.id);
      if (this.multiple) {
        const newValue = this.internalValue.slice(0, index).concat(this.internalValue.slice(index + 1));
        this.$emit("update:modelValue", newValue);
      } else {
        this.$emit("update:modelValue", null);
      }
      if (this.closeOnSelect && shouldClose)
        this.deactivate();
    },
    removeLastElement() {
      if (this.blockKeys.indexOf("Delete") !== -1)
        return;
      if (this.search.length === 0 && Array.isArray(this.internalValue) && this.internalValue.length) {
        this.removeElement(this.internalValue[this.internalValue.length - 1], false);
      }
    },
    activate() {
      if (this.isOpen || this.disabled)
        return;
      this.adjustPosition();
      if (this.groupValues && this.pointer === 0 && this.filteredOptions.length) {
        this.pointer = 1;
      }
      this.isOpen = true;
      if (this.searchable) {
        if (!this.preserveSearch)
          this.search = "";
        this.$nextTick(() => this.$refs.search && this.$refs.search.focus());
      } else {
        this.$el.focus();
      }
      this.$emit("open", this.id);
    },
    deactivate() {
      if (!this.isOpen)
        return;
      this.isOpen = false;
      if (this.searchable) {
        this.$refs.search && this.$refs.search.blur();
      } else {
        this.$el.blur();
      }
      if (!this.preserveSearch)
        this.search = "";
      this.$emit("close", this.getValue(), this.id);
    },
    toggle() {
      this.isOpen ? this.deactivate() : this.activate();
    },
    adjustPosition() {
      if (typeof window === "undefined")
        return;
      const spaceAbove = this.$el.getBoundingClientRect().top;
      const spaceBelow = window.innerHeight - this.$el.getBoundingClientRect().bottom;
      const hasEnoughSpaceBelow = spaceBelow > this.maxHeight;
      if (hasEnoughSpaceBelow || spaceBelow > spaceAbove || this.openDirection === "below" || this.openDirection === "bottom") {
        this.preferredOpenDirection = "below";
        this.optimizedHeight = Math.min(spaceBelow - 40, this.maxHeight);
      } else {
        this.preferredOpenDirection = "above";
        this.optimizedHeight = Math.min(spaceAbove - 40, this.maxHeight);
      }
    }
  }
};
var pointerMixin = {
  data() {
    return {
      pointer: 0,
      pointerDirty: false
    };
  },
  props: {
    showPointer: {
      type: Boolean,
      default: true
    },
    optionHeight: {
      type: Number,
      default: 40
    }
  },
  computed: {
    pointerPosition() {
      return this.pointer * this.optionHeight;
    },
    visibleElements() {
      return this.optimizedHeight / this.optionHeight;
    }
  },
  watch: {
    filteredOptions() {
      this.pointerAdjust();
    },
    isOpen() {
      this.pointerDirty = false;
    },
    pointer() {
      this.$refs.search && this.$refs.search.setAttribute("aria-activedescendant", this.id + "-" + this.pointer.toString());
    }
  },
  methods: {
    optionHighlight(index, option) {
      return {
        "multiselect__option--highlight": index === this.pointer && this.showPointer,
        "multiselect__option--selected": this.isSelected(option)
      };
    },
    groupHighlight(index, selectedGroup) {
      if (!this.groupSelect) {
        return [
          "multiselect__option--disabled",
          { "multiselect__option--group": selectedGroup.$isLabel }
        ];
      }
      const group = this.options.find((option) => {
        return option[this.groupLabel] === selectedGroup.$groupLabel;
      });
      return group && !this.wholeGroupDisabled(group) ? [
        "multiselect__option--group",
        { "multiselect__option--highlight": index === this.pointer && this.showPointer },
        { "multiselect__option--group-selected": this.wholeGroupSelected(group) }
      ] : "multiselect__option--disabled";
    },
    addPointerElement({ key } = "Enter") {
      if (this.filteredOptions.length > 0) {
        this.select(this.filteredOptions[this.pointer], key);
      }
      this.pointerReset();
    },
    pointerForward() {
      if (this.pointer < this.filteredOptions.length - 1) {
        this.pointer++;
        if (this.$refs.list.scrollTop <= this.pointerPosition - (this.visibleElements - 1) * this.optionHeight) {
          this.$refs.list.scrollTop = this.pointerPosition - (this.visibleElements - 1) * this.optionHeight;
        }
        if (this.filteredOptions[this.pointer] && this.filteredOptions[this.pointer].$isLabel && !this.groupSelect)
          this.pointerForward();
      }
      this.pointerDirty = true;
    },
    pointerBackward() {
      if (this.pointer > 0) {
        this.pointer--;
        if (this.$refs.list.scrollTop >= this.pointerPosition) {
          this.$refs.list.scrollTop = this.pointerPosition;
        }
        if (this.filteredOptions[this.pointer] && this.filteredOptions[this.pointer].$isLabel && !this.groupSelect)
          this.pointerBackward();
      } else {
        if (this.filteredOptions[this.pointer] && this.filteredOptions[0].$isLabel && !this.groupSelect)
          this.pointerForward();
      }
      this.pointerDirty = true;
    },
    pointerReset() {
      if (!this.closeOnSelect)
        return;
      this.pointer = 0;
      if (this.$refs.list) {
        this.$refs.list.scrollTop = 0;
      }
    },
    pointerAdjust() {
      if (this.pointer >= this.filteredOptions.length - 1) {
        this.pointer = this.filteredOptions.length ? this.filteredOptions.length - 1 : 0;
      }
      if (this.filteredOptions.length > 0 && this.filteredOptions[this.pointer].$isLabel && !this.groupSelect) {
        this.pointerForward();
      }
    },
    pointerSet(index) {
      this.pointer = index;
      this.pointerDirty = true;
    }
  }
};
var script = {
  name: "vue-multiselect",
  mixins: [multiselectMixin, pointerMixin],
  props: {
    name: {
      type: String,
      default: ""
    },
    modelValue: {
      type: null,
      default() {
        return [];
      }
    },
    selectLabel: {
      type: String,
      default: "Press enter to select"
    },
    selectGroupLabel: {
      type: String,
      default: "Press enter to select group"
    },
    selectedLabel: {
      type: String,
      default: "Selected"
    },
    deselectLabel: {
      type: String,
      default: "Press enter to remove"
    },
    deselectGroupLabel: {
      type: String,
      default: "Press enter to deselect group"
    },
    showLabels: {
      type: Boolean,
      default: true
    },
    limit: {
      type: Number,
      default: 99999
    },
    maxHeight: {
      type: Number,
      default: 300
    },
    limitText: {
      type: Function,
      default: (count) => `and ${count} more`
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    openDirection: {
      type: String,
      default: ""
    },
    showNoOptions: {
      type: Boolean,
      default: true
    },
    showNoResults: {
      type: Boolean,
      default: true
    },
    tabindex: {
      type: Number,
      default: 0
    }
  },
  computed: {
    isSingleLabelVisible() {
      return (this.singleValue || this.singleValue === 0) && (!this.isOpen || !this.searchable) && !this.visibleValues.length;
    },
    isPlaceholderVisible() {
      return !this.internalValue.length && (!this.searchable || !this.isOpen);
    },
    visibleValues() {
      return this.multiple ? this.internalValue.slice(0, this.limit) : [];
    },
    singleValue() {
      return this.internalValue[0];
    },
    deselectLabelText() {
      return this.showLabels ? this.deselectLabel : "";
    },
    deselectGroupLabelText() {
      return this.showLabels ? this.deselectGroupLabel : "";
    },
    selectLabelText() {
      return this.showLabels ? this.selectLabel : "";
    },
    selectGroupLabelText() {
      return this.showLabels ? this.selectGroupLabel : "";
    },
    selectedLabelText() {
      return this.showLabels ? this.selectedLabel : "";
    },
    inputStyle() {
      if (this.searchable || this.multiple && this.modelValue && this.modelValue.length) {
        return this.isOpen ? { width: "100%" } : { width: "0", position: "absolute", padding: "0" };
      }
      return "";
    },
    contentStyle() {
      return this.options.length ? { display: "inline-block" } : { display: "block" };
    },
    isAbove() {
      if (this.openDirection === "above" || this.openDirection === "top") {
        return true;
      } else if (this.openDirection === "below" || this.openDirection === "bottom") {
        return false;
      } else {
        return this.preferredOpenDirection === "above";
      }
    },
    showSearchInput() {
      return this.searchable && (this.hasSingleSelectedSlot && (this.visibleSingleValue || this.visibleSingleValue === 0) ? this.isOpen : true);
    }
  }
};
const _hoisted_1$1 = {
  ref: "tags",
  class: "multiselect__tags"
};
const _hoisted_2$1 = { class: "multiselect__tags-wrap" };
const _hoisted_3$1 = { class: "multiselect__spinner" };
const _hoisted_4$1 = { key: 0 };
const _hoisted_5$1 = { class: "multiselect__option" };
const _hoisted_6 = { class: "multiselect__option" };
const _hoisted_7 = /* @__PURE__ */ createTextVNode("No elements found. Consider changing the search query.");
const _hoisted_8 = { class: "multiselect__option" };
const _hoisted_9 = /* @__PURE__ */ createTextVNode("List is empty.");
function render(_ctx, _cache, $props, $setup, $data, $options) {
  return openBlock(), createBlock("div", {
    tabindex: _ctx.searchable ? -1 : $props.tabindex,
    class: [{ "multiselect--active": _ctx.isOpen, "multiselect--disabled": $props.disabled, "multiselect--above": $options.isAbove }, "multiselect"],
    onFocus: _cache[14] || (_cache[14] = ($event) => _ctx.activate()),
    onBlur: _cache[15] || (_cache[15] = ($event) => _ctx.searchable ? false : _ctx.deactivate()),
    onKeydown: [
      _cache[16] || (_cache[16] = withKeys(withModifiers(($event) => _ctx.pointerForward(), ["self", "prevent"]), ["down"])),
      _cache[17] || (_cache[17] = withKeys(withModifiers(($event) => _ctx.pointerBackward(), ["self", "prevent"]), ["up"]))
    ],
    onKeypress: _cache[18] || (_cache[18] = withKeys(withModifiers(($event) => _ctx.addPointerElement($event), ["stop", "self"]), ["enter", "tab"])),
    onKeyup: _cache[19] || (_cache[19] = withKeys(($event) => _ctx.deactivate(), ["esc"])),
    role: "combobox",
    "aria-owns": "listbox-" + _ctx.id
  }, [
    renderSlot(_ctx.$slots, "caret", { toggle: _ctx.toggle }, () => [
      createVNode("div", {
        onMousedown: _cache[1] || (_cache[1] = withModifiers(($event) => _ctx.toggle(), ["prevent", "stop"])),
        class: "multiselect__select"
      }, null, 32)
    ]),
    renderSlot(_ctx.$slots, "clear", { search: _ctx.search }),
    createVNode("div", _hoisted_1$1, [
      renderSlot(_ctx.$slots, "selection", {
        search: _ctx.search,
        remove: _ctx.removeElement,
        values: $options.visibleValues,
        isOpen: _ctx.isOpen
      }, () => [
        withDirectives(createVNode("div", _hoisted_2$1, [
          (openBlock(true), createBlock(Fragment, null, renderList($options.visibleValues, (option, index) => {
            return renderSlot(_ctx.$slots, "tag", {
              option,
              search: _ctx.search,
              remove: _ctx.removeElement
            }, () => [
              (openBlock(), createBlock("span", {
                class: "multiselect__tag",
                key: index
              }, [
                createVNode("span", {
                  textContent: toDisplayString(_ctx.getOptionLabel(option))
                }, null, 8, ["textContent"]),
                createVNode("i", {
                  tabindex: "1",
                  onKeypress: withKeys(withModifiers(($event) => _ctx.removeElement(option), ["prevent"]), ["enter"]),
                  onMousedown: withModifiers(($event) => _ctx.removeElement(option), ["prevent"]),
                  class: "multiselect__tag-icon"
                }, null, 40, ["onKeypress", "onMousedown"])
              ]))
            ]);
          }), 256))
        ], 512), [
          [vShow, $options.visibleValues.length > 0]
        ]),
        _ctx.internalValue && _ctx.internalValue.length > $props.limit ? renderSlot(_ctx.$slots, "limit", { key: 0 }, () => [
          createVNode("strong", {
            class: "multiselect__strong",
            textContent: toDisplayString($props.limitText(_ctx.internalValue.length - $props.limit))
          }, null, 8, ["textContent"])
        ]) : createCommentVNode("v-if", true)
      ]),
      createVNode(Transition, { name: "multiselect__loading" }, {
        default: withCtx(() => [
          renderSlot(_ctx.$slots, "loading", {}, () => [
            withDirectives(createVNode("div", _hoisted_3$1, null, 512), [
              [vShow, $props.loading]
            ])
          ])
        ]),
        _: 3
      }),
      _ctx.searchable ? (openBlock(), createBlock("input", {
        key: 0,
        ref: "search",
        name: $props.name,
        id: _ctx.id,
        type: "text",
        autocomplete: "off",
        spellcheck: "false",
        placeholder: _ctx.placeholder,
        style: $options.inputStyle,
        value: _ctx.search,
        disabled: $props.disabled,
        tabindex: $props.tabindex,
        onInput: _cache[2] || (_cache[2] = ($event) => _ctx.updateSearch($event.target.value)),
        onFocus: _cache[3] || (_cache[3] = withModifiers(($event) => _ctx.activate(), ["prevent"])),
        onBlur: _cache[4] || (_cache[4] = withModifiers(($event) => _ctx.deactivate(), ["prevent"])),
        onKeyup: _cache[5] || (_cache[5] = withKeys(($event) => _ctx.deactivate(), ["esc"])),
        onKeydown: [
          _cache[6] || (_cache[6] = withKeys(withModifiers(($event) => _ctx.pointerForward(), ["prevent"]), ["down"])),
          _cache[7] || (_cache[7] = withKeys(withModifiers(($event) => _ctx.pointerBackward(), ["prevent"]), ["up"])),
          _cache[9] || (_cache[9] = withKeys(withModifiers(($event) => _ctx.removeLastElement(), ["stop"]), ["delete"]))
        ],
        onKeypress: _cache[8] || (_cache[8] = withKeys(withModifiers(($event) => _ctx.addPointerElement($event), ["prevent", "stop", "self"]), ["enter"])),
        class: "multiselect__input",
        "aria-controls": "listbox-" + _ctx.id
      }, null, 44, ["name", "id", "placeholder", "value", "disabled", "tabindex", "aria-controls"])) : createCommentVNode("v-if", true),
      $options.isSingleLabelVisible ? (openBlock(), createBlock("span", {
        key: 1,
        class: "multiselect__single",
        onMousedown: _cache[10] || (_cache[10] = withModifiers((...args) => _ctx.toggle && _ctx.toggle(...args), ["prevent"]))
      }, [
        renderSlot(_ctx.$slots, "singleLabel", { option: $options.singleValue }, () => [
          createTextVNode(toDisplayString(_ctx.currentOptionLabel), 1)
        ])
      ], 32)) : createCommentVNode("v-if", true),
      $options.isPlaceholderVisible ? (openBlock(), createBlock("span", {
        key: 2,
        class: "multiselect__placeholder",
        onMousedown: _cache[11] || (_cache[11] = withModifiers((...args) => _ctx.toggle && _ctx.toggle(...args), ["prevent"]))
      }, [
        renderSlot(_ctx.$slots, "placeholder", {}, () => [
          createTextVNode(toDisplayString(_ctx.placeholder), 1)
        ])
      ], 32)) : createCommentVNode("v-if", true)
    ], 512),
    createVNode(Transition, { name: "multiselect" }, {
      default: withCtx(() => [
        withDirectives(createVNode("div", {
          class: "multiselect__content-wrapper",
          onFocus: _cache[12] || (_cache[12] = (...args) => _ctx.activate && _ctx.activate(...args)),
          tabindex: "-1",
          onMousedown: _cache[13] || (_cache[13] = withModifiers(() => {
          }, ["prevent"])),
          style: { maxHeight: _ctx.optimizedHeight + "px" },
          ref: "list"
        }, [
          createVNode("ul", {
            class: "multiselect__content",
            style: $options.contentStyle,
            role: "listbox",
            id: "listbox-" + _ctx.id
          }, [
            renderSlot(_ctx.$slots, "beforeList"),
            _ctx.multiple && _ctx.max === _ctx.internalValue.length ? (openBlock(), createBlock("li", _hoisted_4$1, [
              createVNode("span", _hoisted_5$1, [
                renderSlot(_ctx.$slots, "maxElements", {}, () => [
                  createTextVNode("Maximum of " + toDisplayString(_ctx.max) + " options selected. First remove a selected option to select another.", 1)
                ])
              ])
            ])) : createCommentVNode("v-if", true),
            !_ctx.max || _ctx.internalValue.length < _ctx.max ? (openBlock(true), createBlock(Fragment, { key: 1 }, renderList(_ctx.filteredOptions, (option, index) => {
              return openBlock(), createBlock("li", {
                class: "multiselect__element",
                key: index,
                id: _ctx.id + "-" + index,
                role: !(option && (option.$isLabel || option.$isDisabled)) ? "option" : null
              }, [
                !(option && (option.$isLabel || option.$isDisabled)) ? (openBlock(), createBlock("span", {
                  key: 0,
                  class: [_ctx.optionHighlight(index, option), "multiselect__option"],
                  onClick: withModifiers(($event) => _ctx.select(option), ["stop"]),
                  onMouseenter: withModifiers(($event) => _ctx.pointerSet(index), ["self"]),
                  "data-select": option && option.isTag ? _ctx.tagPlaceholder : $options.selectLabelText,
                  "data-selected": $options.selectedLabelText,
                  "data-deselect": $options.deselectLabelText
                }, [
                  renderSlot(_ctx.$slots, "option", {
                    option,
                    search: _ctx.search,
                    index
                  }, () => [
                    createVNode("span", null, toDisplayString(_ctx.getOptionLabel(option)), 1)
                  ])
                ], 42, ["onClick", "onMouseenter", "data-select", "data-selected", "data-deselect"])) : createCommentVNode("v-if", true),
                option && (option.$isLabel || option.$isDisabled) ? (openBlock(), createBlock("span", {
                  key: 1,
                  "data-select": _ctx.groupSelect && $options.selectGroupLabelText,
                  "data-deselect": _ctx.groupSelect && $options.deselectGroupLabelText,
                  class: [_ctx.groupHighlight(index, option), "multiselect__option"],
                  onMouseenter: withModifiers(($event) => _ctx.groupSelect && _ctx.pointerSet(index), ["self"]),
                  onMousedown: withModifiers(($event) => _ctx.selectGroup(option), ["prevent"])
                }, [
                  renderSlot(_ctx.$slots, "option", {
                    option,
                    search: _ctx.search,
                    index
                  }, () => [
                    createVNode("span", null, toDisplayString(_ctx.getOptionLabel(option)), 1)
                  ])
                ], 42, ["data-select", "data-deselect", "onMouseenter", "onMousedown"])) : createCommentVNode("v-if", true)
              ], 8, ["id", "role"]);
            }), 128)) : createCommentVNode("v-if", true),
            withDirectives(createVNode("li", null, [
              createVNode("span", _hoisted_6, [
                renderSlot(_ctx.$slots, "noResult", { search: _ctx.search }, () => [
                  _hoisted_7
                ])
              ])
            ], 512), [
              [vShow, $props.showNoResults && (_ctx.filteredOptions.length === 0 && _ctx.search && !$props.loading)]
            ]),
            withDirectives(createVNode("li", null, [
              createVNode("span", _hoisted_8, [
                renderSlot(_ctx.$slots, "noOptions", {}, () => [
                  _hoisted_9
                ])
              ])
            ], 512), [
              [vShow, $props.showNoOptions && (_ctx.options.length === 0 && !_ctx.search && !$props.loading)]
            ]),
            renderSlot(_ctx.$slots, "afterList")
          ], 12, ["id"])
        ], 36), [
          [vShow, _ctx.isOpen]
        ])
      ]),
      _: 3
    })
  ], 42, ["tabindex", "aria-owns"]);
}
script.render = render;
var vueMultiselect_esm = "";
var Select_vue_vue_type_style_index_0_lang = "";
const _hoisted_1 = {
  class: "w-full",
  "data-cy": "section-tabs"
};
const _hoisted_2 = ["value"];
const _hoisted_3 = ["value"];
const _hoisted_4 = { class: "flex space-x-4 mb-2" };
const _hoisted_5 = ["data-cy", "onClick"];
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "Select",
  props: {
    select: null
  },
  setup(__props) {
    const p = __props;
    const tabNumber = ref(0);
    const sectionType = computed(() => {
      const { type, children } = p.select;
      if (type)
        return type;
      return children.length < 5 ? "tabs" : "dropdown";
    });
    const labels = computed(
      () => p.select.children.map(
        (child, idx) => child.label || `Section ${idx + 1}`
      )
    );
    const tabNumbers = computed(
      () => labels.value.map((_, idx) => idx)
    );
    const currentTree = computed(() => p.select.children[tabNumber.value]);
    const multiSelectCustomLabel = (tabNumber2) => labels.value[tabNumber2];
    const setTabNumber = (val) => tabNumber.value = val;
    const setTabNumberFromEvent = (ev) => void setTabNumber(+ev.target.value);
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("div", _hoisted_1, [
        createElementVNode("div", {
          class: normalizeClass(["w-full mb-2", { "sm:hidden": unref(sectionType) === "tabs" }])
        }, [
          p.select.children.length < 10 ? (openBlock(), createElementBlock("select", {
            key: 0,
            id: "tabs",
            name: "tabs",
            class: "block mb-1 w-auto focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md",
            value: tabNumber.value,
            onChange: setTabNumberFromEvent
          }, [
            (openBlock(true), createElementBlock(Fragment, null, renderList(unref(labels), (label, idx) => {
              return openBlock(), createElementBlock("option", {
                key: idx,
                value: idx
              }, toDisplayString(label), 9, _hoisted_3);
            }), 128))
          ], 40, _hoisted_2)) : (openBlock(), createBlock(unref(script), {
            key: 1,
            modelValue: tabNumber.value,
            "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => tabNumber.value = $event),
            options: unref(tabNumbers),
            "preselect-first": true,
            "clear-on-select": false,
            "allow-empty": false,
            "custom-label": multiSelectCustomLabel
          }, null, 8, ["modelValue", "options"]))
        ], 2),
        createElementVNode("div", {
          class: normalizeClass(["hidden", { "sm:block": unref(sectionType) === "tabs" }])
        }, [
          createElementVNode("nav", _hoisted_4, [
            (openBlock(true), createElementBlock(Fragment, null, renderList(p.select.children, (child, idx) => {
              return openBlock(), createElementBlock("a", {
                role: "button",
                key: idx,
                "data-cy": `tab-${idx}`,
                class: normalizeClass([
                  "px-3 py-2 font-medium text-sm rounded-md",
                  {
                    "text-dp-accent bg-dp-accent-light": tabNumber.value === idx,
                    "text-dp-light-gray hover:text-dp-dark-gray": tabNumber.value !== idx
                  }
                ]),
                onClick: () => setTabNumber(idx)
              }, toDisplayString(unref(labels)[idx]), 11, _hoisted_5);
            }), 128))
          ])
        ], 2),
        createElementVNode("div", null, [
          renderSlot(_ctx.$slots, "default", { tree: unref(currentTree) })
        ])
      ]);
    };
  }
});
export { _sfc_main as default };
