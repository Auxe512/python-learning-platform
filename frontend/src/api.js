import axios from 'axios'

const BASE_URL = 'https://python-learning-platform-quf0.onrender.com'

export async function submitCode(code) {
  const response = await axios.post(`${BASE_URL}/submit`, { code })
  return response.data  // { results: [...], hint: string|null }
}
