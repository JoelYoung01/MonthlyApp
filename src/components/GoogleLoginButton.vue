<script setup lang="ts">
import { inject, nextTick, useTemplateRef } from "vue";
import { googleAccountsLoadedKey } from "@/plugins/googleAuth";

type ViewType = "signin" | "signup" | "use";
interface Props {
  view: ViewType;
}

const props = withDefaults(defineProps<Props>(), {
  view: "signup"
});

const viewToText: Record<ViewType, google.accounts.id.GsiButtonConfiguration["text"]> = {
  signin: "signin_with",
  signup: "signup_with",
  use: "signin"
};

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
    text: viewToText[props.view],
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
