<script setup lang="ts">
import { inject, nextTick, useTemplateRef } from "vue";
import { googleAccountsLoadedKey } from "@/plugins/googleAuth";

const loaded = inject(googleAccountsLoadedKey, ref());
const button = useTemplateRef("button");

function render() {
  if (button.value === null) {
    throw new Error("No button found when attempting to render google login button.");
  }

  google.accounts.id.renderButton(button.value, {
    type: "standard",
    theme: "outline",
    size: "large",
    text: "signin_with",
    shape: "rectangular"
  });
}

watch(
  loaded,
  (newValue) => {
    if (newValue) {
      nextTick(render);
    }
  },
  {
    immediate: true
  }
);
</script>

<template>
  <div ref="button"></div>
</template>
