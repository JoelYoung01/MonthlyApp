<script setup lang="ts">
import { User } from "@lucide/vue";
import { useSessionStore } from "@/stores/session";
import { useRouter } from "vue-router";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog";

const sessionStore = useSessionStore();
const router = useRouter();

const dialogOpen = ref(false);

function logout() {
  sessionStore.logout();
  dialogOpen.value = false;
  router.push("/login");
}
</script>

<template>
  <Dialog v-if="sessionStore.currentUser" v-model:open="dialogOpen">
    <DialogTrigger as-child>
      <Button
        variant="ghost"
        size="icon"
        class="rounded-full text-primary-foreground hover:bg-primary-foreground/10"
      >
        <Avatar size="sm">
          <AvatarImage :src="sessionStore.currentUser.avatar_url ?? ''" alt="Profile Image" />
          <AvatarFallback>
            <User class="size-4" />
          </AvatarFallback>
        </Avatar>
      </Button>
    </DialogTrigger>
    <DialogContent class="sm:max-w-xs">
      <DialogHeader>
        <DialogTitle class="text-center">Account</DialogTitle>
      </DialogHeader>
      <div class="flex flex-col items-center gap-3 py-2">
        <Avatar size="lg">
          <AvatarImage :src="sessionStore.currentUser.avatar_url ?? ''" alt="Profile Image" />
          <AvatarFallback>
            <User class="size-8" />
          </AvatarFallback>
        </Avatar>
        <p class="text-sm font-medium">{{ sessionStore.currentUser.display_name }}</p>
        <Button class="mt-2 w-full" @click="logout">Sign Out</Button>
      </div>
    </DialogContent>
  </Dialog>
</template>
