<script setup> 
import { RouterLink, RouterView } from 'vue-router'
import { Icon } from '@iconify/vue'
import { Heart } from '@lucide/vue'

const links = [
  { label: 'создать', to: '/' },
  { label: 'мои ссылки', to: '/links' },
]

</script>

<template>
  <div class="flex flex-col min-h-screen selection:bg-black selection:text-white">
    <header class="pt-5 px-10 border-b border-slate-200 flex flex-row justify-between items-end">
      <span class="font-mono font-semibold tracking-tight text-lg text-slate-900 pb-4">
        url.shorten()
      </span>

      <div class="flex flex-row font-mono uppercase justify-end font-semibold gap-15">
        
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" v-slot="{ isActive }" class="pb-4.5 relative group">
          <span :class="isActive ? 'text-slate-900' : 'text-slate-400 group-hover:text-slate-700 transition-colors duration-300'">
            {{ link.label }}
          </span>

          <div class="absolute bottom-0 left-0 h-0.75 bg-slate-900 transition-all duration-300 origin-center" :class="isActive ? 'w-full scale-x-100' : 'w-full scale-x-0 group-hover:scale-x-100'" />
        </RouterLink>
      </div>
    </header>

    <main class="grow">
      <RouterView />
    </main>

    <footer class="border-t border-slate-100 bg-white px-10 py-7">
      <div class="mx-auto grid grid-cols-1 gap-8 sm:grid-cols-3">
        <div class="flex flex-col justify-between space-y-4 sm:space-y-0">
          <div>
            <span class="font-mono text-lg font-semibold tracking-tight text-slate-900 block pb-1">
              url.shorten()
            </span>

            <span class="font-mono text-sm font-medium text-slate-600 leading-relaxed block">
              Простой сервис для сокращения ссылок
            </span>
          </div>

          <span class="font-mono font-medium text-sm text-slate-600">
            &copy; 0x4d8e4854
          </span>
        </div>

        <div class="flex flex-col space-y-3 sm:items-center">
          <div class="flex flex-col space-y-2.5">
            <a href="#" class="font-mono text-sm font-medium text-slate-600 transition-colors duration-200 hover:text-slate-950">
              О сервисе
            </a>
            <a href="#" class="font-mono text-sm font-medium text-slate-600 transition-colors duration-200 hover:text-slate-950">
              Как это работает
            </a>
            <a href="#" class="font-mono text-sm font-medium text-slate-600 transition-colors duration-200 hover:text-slate-950">
              API
            </a>
            <a href="#" class="font-mono text-sm font-medium text-slate-600 transition-colors duration-200 hover:text-slate-950">
              Поддержка
            </a>
          </div>
        </div>

        <div class="flex flex-col justify-between items-start sm:items-end space-y-10 sm:space-y-0">
          <div class="flex items-center gap-8.5 text-black transition-all duration-200">
            <a href="#" class="duration-200 hover:scale-90 hover:text-slate-400">
              <Icon icon="simple-icons:github" width="32" />
            </a>

            <a href="#" class="duration-200 hover:text-slate-600 hover:scale-90">
              <Icon icon="simple-icons:telegram" width="32" />
            </a>

            <a href="#" class="duration-200 hover:text-slate-600 hover:scale-90">
              <Icon icon="lucide:mail" width="32" />
            </a>
          </div>
          
          <span class="font-mono text-sm font-medium text-slate-600 text-right">
            Сделано с любовью <Heart color="black" size="14" fill="black" class="animate-pulse inline mb-1" /><br>в минимализме
          </span>
        </div>

      </div>
    </footer>
  </div>
</template>