<template>
  <q-page class="flex flex-center bg-login">
    <q-card class="q-pa-lg login-card" style="width: 450px; max-width: 90vw">
      <div class="row items-center q-mb-md">
        <q-avatar size="40px">
          <img src="/icons/PCPEtransparente.png" />
        </q-avatar>
        <div class="q-ml-sm text-subtitle1 text-weight-bold text-black">Automação de Cadastro</div>
      </div>

      <q-form @submit="cadastrar" greedy>
        <q-input
          filled
          v-model="nome"
          label="Nome"
          :rules="[(val) => !!val || 'Campo Obrigatório!']"
          class="q-mb-sm"
          input-class="text-black"
        >
          <template v-slot:label><span class="text-black">Nome</span></template>
        </q-input>

        <q-input
          filled
          v-model="matricula"
          label="Matrícula"
          @update:model-value="(val) => (matricula = val.replace(/\D/g, ''))"
          :rules="[(val) => !!val || 'Campo Obrigatório!']"
          class="q-mb-sm"
          input-class="text-black"
        >
          <template v-slot:label><span class="text-black">Matrícula</span></template>
        </q-input>

        <q-input
          filled
          v-model="cpf"
          label="CPF"
          mask="###.###.###-##"
          unmasked-value
          :rules="[(val) => (val && val.length === 11) || 'CPF inválido!']"
          class="q-mb-sm"
          input-class="text-black"
        >
          <template v-slot:label><span class="text-black">CPF</span></template>
        </q-input>

        <q-select
          filled
          v-model="unidades"
          :options="opcoesUnidades"
          label="Unidades"
          multiple
          emit-value
          map-options
          :rules="[(val) => (val && val.length > 0) || 'Campo Obrigatório!']"
          class="q-mb-sm"
          popup-content-class="text-black"
        >
          <template v-slot:label><span class="text-black">Unidades</span></template>
        </q-select>

        <q-select
          filled
          v-model="sistemas"
          :options="opcoesSistemas"
          label="Sistemas"
          multiple
          emit-value
          map-options
          :rules="[(val) => (val && val.length > 0) || 'Campo Obrigatório!']"
          class="q-mb-md"
          popup-content-class="text-black"
        >
          <template v-slot:label><span class="text-black">Sistemas</span></template>
        </q-select>

        <q-btn label="CADASTRAR" type="submit" class="full-width bg-black text-white q-mb-sm" />
      </q-form>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const nome = ref('')
const matricula = ref('')
const cpf = ref('')
const sistemas = ref([])
const unidades = ref([])

const opcoesSistemas = [
  { label: 'Infopol', value: 'infopol' },
  { label: 'SGTI', value: 'sgti' },
  { label: 'SCPP', value: 'scpp' },
  { label: 'Legis', value: 'legis' },
]

const opcoesUnidades = [
  { label: 'Departamento de Homicídio e Proteção à Pessoa', value: 'dhpp' },
  { label: 'Academia de Polícia', value: 'acadepol' },
  { label: 'Central Plantão Capital', value: 'cpc' },
  { label: 'Comando de Operações e Recurso Especiais', value: 'core' },
  { label: 'Corregedoria Geral da SDS', value: 'corregedoria_sds' },
]

const router = useRouter()

async function cadastrar() {
  try {
    const response = await fetch('http://localhost:3000/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nome: nome.value,
        matricula: matricula.value,
        cpf: cpf.value,
        sistemas: sistemas.value,
        unidades: unidades.value,
      }),
    })
    const data = await response.json()
    if (response.ok && data.success) {
      alert('Cadastro realizado com sucesso')
      router.push('/')
    } else {
      alert(data.message || 'Erro no cadastro')
    }
  } catch (err) {
    alert(`Erro de conexão: ${err.message}`)
  }
}
</script>

<style scoped>
.bg-login {
  background-image: url('/icons/PCPEtransparente.png');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
}
.login-card {
  background: rgba(255, 255, 255, 0.8) !important;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}
.text-black {
  color: black !important;
}
</style>
