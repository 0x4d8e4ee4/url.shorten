<script setup>
import Modal from '@/components/Modal.vue'
import { ref } from 'vue'
import { LinkIcon, ChevronDownIcon, LoaderCircleIcon, QrCodeIcon } from '@lucide/vue'
import axios from 'axios'

const link = ref('')
const loading = ref(false)
const shortSlug = ref('')
const copied = ref(false)
const openSettings = ref(false)
const isOpenModal = ref(false)

const handleSubmit = async () => {
  const cleanLink = link.value.trim().replace(/^https?:\/\//, '')
  if (!cleanLink) {
    alert(cleanLink)
    return
  }
  
  loading.value = true
  try {
    const response = await axios.post('http://localhost:8000/generate', { url: cleanLink })
    
    shortSlug.value = response.data.slug
    link.value = ''
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const copyUrl = async (text) => {
  try {
    copied.value = true
    await navigator.clipboard.writeText(text);
    setTimeout(() => {
      copied.value = false
    }, 3000);
  } catch (err) {
    console.error('Не удалось скопировать: ', err);
  }
};

</script>

<template>
  <div class="flex flex-col text-center font-mono font-semibold tracking-wide text-5xl mt-25">
    <span>Сокращай ссылки<br>и делись легко.</span>
  </div>

  <div class="text-center font-mono mt-7 text-slate-600 font-medium text-lg leading-6">
    <span>Превращай нечитабельные ссылки в короткие<br>и отслеживай каждый клик.</span>
  </div>

  <div class="flex flex-row lg:w-240 sm:w-3/4 mx-auto h-16 border-2 mt-10 items-center">
    <div class="flex justify-center items-center h-full px-4.5 border-r-2">
      <LinkIcon :stroke-width="1.5" class="w-6 h-6" />
    </div>
    
    <input type="text" placeholder="Вставьте длинную ссылку" v-model="link" class="p-5 w-full focus:outline-none font-mono font-medium text-sm placeholder:text-slate-600">
    
    <button class="bg-black w-48 border-l-2 h-full uppercase text-white font-mono cursor-pointer hover:bg-white hover:text-black transition-all duration-300" @click="handleSubmit">
      <LoaderCircleIcon v-if="loading" size="20" class="animate-spin inline text-black transition-all duration-300" />
      <span v-else class="">создать</span>
    </button>
  </div>

  <div class="flex items-center justify-center lg:w-240 sm:w-3/4 mx-auto my-10">
    <div class="grow border-t-2"></div>
    <button @click="openSettings = !openSettings" class="flex flex-row">
      <span class="ml-4 font-mono text-sm font-semibold text-black uppercase tracking-wider whitespace-nowrap">дополнительные настройки</span>
      <ChevronDownIcon size="16" class="mx-4" />
    </button>
    <div class="grow border-t-2"></div>
  </div>

  <div v-if="openSettings" class="grid grid-cols-2 gap-7 w-240 mx-auto my-10 p-10 border-2 font-mono shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
    
    <div class="flex flex-col gap-1">
      <span class="font-medium text-sm">Пользовательская ссылка</span>
      <div class="flex flex-row items-center border-2">
        <span class="inline-block pl-4 py-3.5 font-medium text-sm">civacel.io/</span>
        <input type="text" class="font-medium h-full text-sm focus:outline-none placeholder:text-slate-600" placeholder="shortslug">
      </div>
    </div>

    <div class="flex flex-col gap-1">
      <span class="font-medium text-sm">Срок действия</span>
      <input type="text" class="border-2 font-medium py-3.5 px-4 text-sm focus:outline-none placeholder:text-slate-600" placeholder="Без срока действия">
    </div>

    <div class="flex flex-col gap-1">
      <span class="font-medium text-sm">Защита паролем</span>
      <input type="password" class="border-2 font-medium py-3.5 px-4 text-sm focus:outline-none placeholder:text-slate-600" placeholder="Введите пароль">
    </div>

    <div class="flex flex-col gap-1">
      <span class="font-medium text-sm">Заметки</span>
      <input type="text" class="border-2 font-medium py-3.5 px-4 text-sm focus:outline-none placeholder:text-slate-600" placeholder="Введите ссылку">
    </div>

  </div>

  <div v-if="shortSlug" class="flex flex-row lg:w-240 sm:w-3/4 mx-auto h-16 border-2 items-center">
    <button class="flex cursor-pointer justify-center items-center h-full px-4.5 border-r-2 transition-all duration-300 hover:bg-black hover:text-white" @click="isOpenModal = true">
      <QrCodeIcon :stroke-width="1.3" class="w-6 h-6" />
    </button>
    <Modal :isOpen="isOpenModal" @close="isOpenModal = false">
      <template #header>
        <span class="font-mono font-bold uppercase tracking-wider text-base">
          QR Код Ссылки
        </span>
      </template>

      <div class="flex flex-col items-center justify-center p-2 bg-white">
        <div class="border-2 border-black p-3 bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
          <img 
            :src="`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://civacel.io/${shortSlug}`" 
            alt="QR Code" 
            class="w-37.5 h-37.5 block filter grayscale contract-125"
          />
        </div>
        <p class="mt-7 text-xs text-center text-zinc-500 selection:bg-black selection:text-white">
          https://civacel.io/{{ shortSlug }}
        </p>
      </div>

      <template #footer>
        <a :href="`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://civacel.io/${shortSlug}`" :download="`qr-code-${shortSlug}.png`" class="px-4 py-2 border-2 border-black bg-white text-black font-mono font-medium uppercase text-xs tracking-wider hover:bg-black hover:text-white transition-colors duration-200 cursor-pointer">
          скачать
        </a>
        <button @click="isOpenModal = false" class="px-4 py-2 border-2 border-black bg-black text-white font-mono font-medium uppercase text-xs tracking-wider hover:bg-white hover:text-black transition-colors duration-200 cursor-pointer">
          готово
        </button>
      </template>
    </Modal>

    <span class="p-5 w-full focus:outline-none font-mono font-medium text-sm placeholder:text-slate-600">civacel.io/{{ shortSlug }}</span>
    
    <button v-if="copied" class="w-48 border-l-2 border-black h-full uppercase text-black font-mono" :disabled="copied">
      <span>скопировано</span>
    </button>

    <button v-else class="w-48 border-l-2 border-black cursor-pointer h-full uppercase text-black font-mono hover:bg-black hover:text-white transition-all duration-300" @click="copyUrl(`https://civacel.io/${shortSlug}`)">
      <span>копировать</span>
    </button>
  </div>
</template>