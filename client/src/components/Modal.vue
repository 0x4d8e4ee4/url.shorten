<!-- Modal.vue -->
<script setup>

defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-[9999] flex items-center justify-center backdrop-blur-[2px] p-4 transition-all duration-300"
      @click.self="emit('close')"
    >
      <div class="bg-white border-2 border-black rounded-none shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] w-full max-w-md flex flex-col overflow-hidden">
        <header class="flex items-center justify-between border-b-2 border-black px-5 py-4 bg-white select-none">
          <slot name="header">
            <span class="font-mono font-bold uppercase tracking-wider text-black text-sm">Уведомление</span>
          </slot>

          <button 
            @click="emit('close')" 
            class="text-black font-mono font-bold text-xl hover:bg-black hover:text-white px-2 py-0.5 border border-transparent hover:border-black transition-colors duration-200 cursor-pointer"
          >
            &times;
          </button>
        </header>

        <main class="px-5 py-6 bg-white text-black font-mono text-sm leading-relaxed">
          <slot>Дефолтное содержимое окна.</slot>
        </main>

        <footer class="border-t-2 border-black px-5 py-4 bg-white flex justify-end gap-3">
          <slot name="footer">
            <button 
              @click="emit('close')" 
              class="px-4 py-2 border-2 border-black bg-black text-white font-mono font-bold uppercase text-xs tracking-wider hover:bg-white hover:text-black transition-colors duration-200 cursor-pointer"
            >
              Закрыть
            </button>
          </slot>
        </footer>
      </div>
    </div>
  </Teleport>
</template>
