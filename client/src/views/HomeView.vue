<script setup>
import { ref } from 'vue'
import { LinkIcon, ChevronDownIcon, LoaderCircleIcon } from '@lucide/vue'
import axios from 'axios'

const link = ref('')
const loading = ref(false)
const shortLink = ref('')

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

</script>

<template>
  <div class="flex flex-col text-center font-mono font-semibold tracking-wide text-5xl mt-25">
    <span>Сокращай ссылки<br>и делись легко.</span>
  </div>

  <div class="text-center font-mono mt-7 text-slate-600 font-medium text-lg leading-6">
    <span>Превращай нечитабельные ссылки в короткие<br>и отслеживай каждый клик.</span>
  </div>

  <div class="flex flex-row lg:w-240 sm:w-3/4 mx-auto h-16 border mt-10 items-center pl-5">
    <LinkIcon size="24"/>
    <input type="text" placeholder="Вставьте длинную ссылку" v-model="link" class="p-5 w-full focus:outline-none font-mono font-medium text-sm placeholder:text-slate-600">
    <button class="bg-black w-48 h-full uppercase text-white font-mono" @click="handleSubmit">
      <LoaderCircleIcon v-if="loading" size="20" class="animate-spin inline" />
      <span v-else>создать</span>
    </button>
  </div>

  <div class="flex items-center justify-center lg:w-240 sm:w-3/4 mx-auto mt-10 mb-60">
    <div class="grow border-t"></div>
    <span class="ml-4 font-mono text-sm font-semibold text-black uppercase tracking-wider whitespace-nowrap">дополнительные настройки</span>
    <ChevronDownIcon size="16" class="mx-4" />
    <div class="grow border-t"></div>
  </div>

  <div v-if="shortLink" class="bg-green-300/50 text-white font-medium font-mono">
    <span>{{ shortLink }}</span>
  </div>
</template>
