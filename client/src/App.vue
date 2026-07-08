<script setup>
import '@/assets/main.css'
import { ref, computed, watch } from 'vue'

const API_BASE_URL = 'http://localhost:8000'

const BAR_SCALE = 60

const longUrl = ref('')
const shortUrl = ref('')
const slug = ref('')
const submittedLength = ref(0)

const isLoading = ref(false)
const errorMessage = ref('')
const copied = ref(false)

const displayShortUrl = computed(() =>
  shortUrl.value.replace(/^https?:\/\//i, '')
)

const codeLength = computed(() => slug.value.length)

const ratio = computed(() => {
  if (!codeLength.value) return 1

  return Math.max(
    1,
    Math.round(submittedLength.value / codeLength.value)
  )
})

const ratioWord = computed(() => razWord(ratio.value))

const originalBarWidth = computed(() =>
  Math.min(
    100,
    (submittedLength.value / BAR_SCALE) * 100
  )
)

const codeBarWidth = computed(() =>
  Math.min(
    100,
    (codeLength.value / BAR_SCALE) * 100
  )
)

watch(longUrl, () => {
  if (errorMessage.value) {
    errorMessage.value = ''
  }
})

function razWord(n) {
  const mod100 = n % 100
  const mod10 = n % 10

  if (mod100 >= 11 && mod100 <= 14) {
    return 'раз'
  }

  if (mod10 === 1) {
    return 'раз'
  }

  if (mod10 >= 2 && mod10 <= 4) {
    return 'раза'
  }

  return 'раз'
}

function normalizeUrl(value) {
  return value
    .trim()
    .replace(/^https?:\/\//i, '')
}

function looksLikeUrl(value) {
  return /\.[a-z]{2,}/i.test(value)
}

async function handleSubmit() {
  const trimmed = longUrl.value.trim()

  if (!trimmed) {
    errorMessage.value = 'Введите ссылку'
    return
  }

  const normalized = normalizeUrl(trimmed)

  if (!looksLikeUrl(normalized)) {
    errorMessage.value =
      'Похоже, это не ссылка. Проверьте адрес'
    return
  }

  copied.value = false
  errorMessage.value = ''
  shortUrl.value = ''
  isLoading.value = true

  try {
    const response = await fetch(
      `${API_BASE_URL}/generate`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: normalized
        })
      }
    )

    if (!response.ok) {
      throw new Error()
    }

    const payload = await response.json()

    const receivedSlug = payload?.data?.message

    if (!receivedSlug) {
      throw new Error()
    }

    slug.value = receivedSlug
    submittedLength.value = trimmed.length
    shortUrl.value = `${API_BASE_URL}/${receivedSlug}`
  } catch (e) {
    errorMessage.value =
      'Не получилось создать ссылку. Проверьте бекенд и повторите попытку.'
  } finally {
    isLoading.value = false
  }
}

async function copyLink() {
  if (!shortUrl.value) {
    return
  }

  try {
    await navigator.clipboard.writeText(shortUrl.value)

    copied.value = true

    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (e) {
    errorMessage.value =
      'Не удалось скопировать ссылку.'
  }
}
</script>

<template>
  <div class="min-h-screen bg-white flex items-center justify-center p-6">
    <div
      class="w-full max-w-110 rounded-2xl border border-zinc-200 bg-white px-9 py-10 shadow-[0_1px_2px_rgba(0,0,0,.04),0_16px_40px_rgba(0,0,0,.06)]"
    >
      <header class="mb-8">
        <h1 class="font-mono text-2xl font-bold tracking-tight">
          url.shorten()
        </h1>

        <p class="mt-2 text-sm leading-6 text-zinc-500">
          Вставьте длинную ссылку — получите короткий код
        </p>
      </header>

      <form
        novalidate
        @submit.prevent="handleSubmit"
      >
        <label
          for="url-input"
          class="mb-2 block text-[11px] font-semibold uppercase tracking-[0.08em] text-zinc-500"
        >
          Ссылка
        </label>

        <div class="flex gap-2 max-[480px]:flex-col">
          <input
            id="url-input"
            v-model="longUrl"
            type="text"
            autocomplete="off"
            placeholder="example.com/very/long/path"
            :disabled="isLoading"
            class="flex-1 rounded-xl border-[1.5px] border-zinc-200 bg-white px-4 py-3 text-sm text-black outline-none transition-colors duration-150 placeholder:text-zinc-400 focus:border-black disabled:opacity-60"
          />

          <button
            type="submit"
            :disabled="isLoading || !longUrl.trim()"
            :aria-label="isLoading ? 'Загрузка' : 'Сократить ссылку'"
            class="min-w-27 rounded-xl border-[1.5px] border-black bg-black px-5 py-3 text-sm font-semibold text-white transition hover:opacity-85 active:scale-95 disabled:cursor-not-allowed disabled:opacity-35"
          >
            <span v-if="!isLoading">
              Сократить
            </span>

            <span
              v-else
              class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
            />
          </button>
        </div>

        <div class="mt-2 min-h-5 pl-1">
          <p
            v-if="errorMessage"
            class="border-l-2 border-black pl-2 text-sm"
          >
            {{ errorMessage }}
          </p>

          <span
            v-else-if="longUrl && !shortUrl"
            class="block text-right font-mono text-xs text-zinc-500"
          >
            {{ longUrl.length }} симв.
          </span>
        </div>
      </form>

      <Transition
        enter-active-class="transition-all duration-200 ease-out"
        enter-from-class="translate-y-2 opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition-all duration-150 ease-in"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-2 opacity-0"
      >
        <div
          v-if="shortUrl"
          class="mt-7 border-t border-zinc-200 pt-7"
        >
          <div
            class="mb-5 flex items-center gap-3 rounded-xl border-[1.5px] border-black p-3"
          >
            <a
              :href="shortUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="flex-1 truncate font-mono text-sm text-black hover:underline"
            >
              {{ displayShortUrl }}
            </a>

            <button
              type="button"
              @click="copyLink"
              :class="[
                'flex h-8 w-8 items-center justify-center rounded-lg transition',
                copied ? 'bg-black/10' : 'hover:bg-black/5'
              ]"
            >
              <svg
                v-if="!copied"
                viewBox="0 0 24 24"
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <rect
                  x="9"
                  y="9"
                  width="13"
                  height="13"
                  rx="2"
                />
                <path
                  d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"
                />
              </svg>

              <svg
                v-else
                viewBox="0 0 24 24"
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <span
                class="w-11 shrink-0 text-[11px] uppercase tracking-wider text-zinc-500"
              >
                было
              </span>

              <div class="h-1.5 flex-1 overflow-hidden rounded bg-zinc-200">
                <div
                  class="h-full rounded bg-black transition-all"
                  :style="{ width: originalBarWidth + '%' }"
                />
              </div>

              <span
                class="w-8 text-right font-mono text-xs text-zinc-500"
              >
                {{ submittedLength }}
              </span>
            </div>

            <div class="flex items-center gap-3">
              <span
                class="w-11 shrink-0 text-[11px] uppercase tracking-wider text-zinc-500"
              >
                стало
              </span>

              <div class="h-1.5 flex-1 overflow-hidden rounded bg-zinc-200">
                <div
                  class="h-full rounded bg-black transition-all"
                  :style="{ width: codeBarWidth + '%' }"
                />
              </div>

              <span
                class="w-8 text-right font-mono text-xs text-zinc-500"
              >
                {{ codeLength }}
              </span>
            </div>

            <p class="pt-2 text-sm font-semibold">
              короче в {{ ratio }} {{ ratioWord }}
            </p>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>