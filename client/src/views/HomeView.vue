<script setup>
import { ref } from 'vue'
import { LinkIcon, ChevronDownIcon, LoaderCircleIcon, QrCodeIcon } from '@lucide/vue'
import axios from 'axios'

const link = ref('')
const loading = ref(false)
const shortLink = ref('')
const copied = ref(false)

const handleSubmit = async () => {
  const cleanLink = link.value.trim().replace(/^https?:\/\//, '')
  if (!cleanLink) {
    alert(cleanLink)
    return
  }
  
  loading.value = true
  try {
    const response = await axios.post('http://localhost:8000/generate', { url: cleanLink })
    
    shortLink.value = 'https://civacel.io/' + response.data.slug
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

  <div class="flex flex-row lg:w-240 sm:w-3/4 mx-auto h-16 border mt-10 items-center">
    <div class="flex justify-center items-center h-full px-4.5 border-r">
      <LinkIcon :stroke-width="1.5" class="w-6 h-6" />
    </div>
    
    <input type="text" placeholder="Вставьте длинную ссылку" v-model="link" class="p-5 w-full focus:outline-none font-mono font-medium text-sm placeholder:text-slate-600">
    
    <button class="bg-black w-48 border-l h-full uppercase text-white font-mono cursor-pointer hover:bg-white hover:text-black transition-all duration-300" @click="handleSubmit">
      <LoaderCircleIcon v-if="loading" size="20" class="animate-spin inline text-black transition-all duration-300" />
      <span v-else class="">создать</span>
    </button>
  </div>

  <div class="flex items-center justify-center lg:w-240 sm:w-3/4 mx-auto my-10">
    <div class="grow border-t"></div>
    <span class="ml-4 font-mono text-sm font-semibold text-black uppercase tracking-wider whitespace-nowrap">дополнительные настройки</span>
    <ChevronDownIcon size="16" class="mx-4" />
    <div class="grow border-t"></div>
  </div>

  <div class="flex flex-row lg:w-240 sm:w-3/4 mx-auto h-16 border mt-10 items-center">
    <div class="flex cursor-pointer justify-center items-center h-full px-4.5 border-r transition-all duration-300 hover:bg-black hover:text-white">
      <QrCodeIcon :stroke-width="1.3" class="w-6 h-6" />
    </div>
    
    <span class="p-5 w-full focus:outline-none font-mono font-medium text-sm placeholder:text-slate-600">civacel.io/shorturl</span>
    
    <button v-if="copied" class="w-48 border-l border-black h-full uppercase text-black font-mono" :disabled="copied">
      <span>скопировано</span>
    </button>

    <button v-else class="w-48 border-l border-black cursor-pointer h-full uppercase text-black font-mono hover:bg-black hover:text-white transition-all duration-300" @click="copyUrl('https://civacel.io/shorturl')">
      <span>копировать</span>
    </button>
  </div>
</template>