<template>
  <q-page class="flex flex-center bg-login">
    <q-card class="q-pa-lg login-card" style="width: 450px; max-width: 90vw">
      <div class="row items-center q-mb-md">
        <q-avatar size="40px">
          <img src="/icons/PCPEtransparente.png" />
        </q-avatar>
        <div class="q-ml-sm text-subtitle1 text-weight-bold text-black">LEGIS-PCPE - CADASTRO</div>
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
          <template v-slot:label>
            <span class="text-black">Nome</span>
          </template>
        </q-input>

        <q-input
          filled
          v-model="matricula"
          label="Matrícula"
          @update:model-value="(val) => (matricula = val.replace(/\D/g, ''))"
          :rules="[
            (val) => !!val || 'Campo Obrigatório!',
            (val) => /^\d+$/.test(val) || 'Apenas números permitidos!',
          ]"
          class="q-mb-sm"
          input-class="text-black"
        >
          <template v-slot:label>
            <span class="text-black">Matrícula</span>
          </template>
        </q-input>
        <q-input
          filled
          v-model="cpf"
          label="CPF"
          mask="###.###.###-##"
          unmasked-value
          :rules="[(val) => (val && val.length === 11) || 'CPF deve conter 11 dígitos!']"
          class="q-mb-md"
          input-class="text-black"
        >
          <template v-slot:label>
            <span class="text-black">CPF</span>
          </template>
        </q-input>

        <q-btn label="CADASTRAR" type="submit" class="full-width bg-black text-white q-mb-sm" />
      </q-form>

      <div class="text-caption text-center q-mt-md text-black">Página de Testes</div>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const nome = ref('')
const matricula = ref('')
const cpf = ref('')
const router = useRouter()

async function cadastrar() {
  if (nome.value && matricula.value && cpf.value) {
    try {
      const response = await fetch('http://localhost:3000/cadastro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome: nome.value,
          matricula: matricula.value,
          cpf: cpf.value,
        }),
      })
      const data = await response.json()
      if (response.ok && data.success) {
        alert('Cadastro realizado com sucesso')
        router.push('/')
      } else {
        alert(data.message || 'Erro ao processar o cadastro')
      }
    } catch (err) {
      alert(`Erro ao conectar ao servidor: ${err.message}`)
    }
  } else {
    alert('Preencha todos os campos corretamente.')
  }
}
</script>

<style scoped>
.bg-login {
  background-image: url('/Public/icons/PCPEtransparente.png');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  backdrop-filter: blur(8px);
}

.login-card {
  background: rgba(255, 255, 255, 0.8) !important;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Força o texto a permanecer preto no modo escuro */
.text-black {
  color: black !important;
}
</style>
