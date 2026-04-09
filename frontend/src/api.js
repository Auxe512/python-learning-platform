import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

export async function submitCode(code) {
  const response = await axios.post(`${BASE_URL}/submit`, { code })
  return response.data  // { results: [...], hint: string|null }
}
