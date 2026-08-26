/**
 * Centralized API Client for AI Medicine Analyzer Backend
 */

const getApiBase = () => {
  const envUrl = (import.meta.env.VITE_API_URL || '').trim().replace(/\/+$/, '');
  if (!envUrl) return '/api';
  return envUrl.endsWith('/api') ? envUrl : `${envUrl}/api`;
};

const API_BASE = getApiBase();


export async function fetchJson(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      },
      ...options
    });

    const contentType = response.headers.get('content-type') || '';
    let data;
    if (contentType.includes('application/json')) {
      data = await response.json();
    } else {
      const text = await response.text();
      if (!response.ok) {
        throw new Error(
          `Backend connection error (${response.status}). Please check VITE_API_URL or ensure backend is running.`
        );
      }
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error('Received non-JSON response from backend.');
      }
    }

    if (!response.ok) {
      throw new Error(data.message || data.error || `HTTP error ${response.status}`);
    }
    return data;
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

// 1. Health & Dashboard Stats
export const checkHealth = () => fetchJson('/health');
export const getDashboardStats = () => fetchJson('/stats');

// 2. Medicine Lookups
export const searchMedicines = (q) => fetchJson(`/medicine/search?q=${encodeURIComponent(q)}`);
export const getMedicineByName = (name) => fetchJson(`/medicine/${encodeURIComponent(name)}`);
export const analyzeMedicine = (medicine_name) => 
  fetchJson('/medicine/analyze', {
    method: 'POST',
    body: JSON.stringify({ medicine_name })
  });

export const analyzeMedicineImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch(`${API_BASE}/medicine/image`, {
    method: 'POST',
    body: formData
  });

  const contentType = response.headers.get('content-type') || '';
  let data;
  if (contentType.includes('application/json')) {
    data = await response.json();
  } else {
    const text = await response.text();
    if (!response.ok) {
      throw new Error(`Backend error (${response.status}). Failed to analyze image.`);
    }
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error('Invalid response from OCR server.');
    }
  }

  if (!response.ok) {
    throw new Error(data.message || data.error || 'Failed to analyze medicine image');
  }
  return data;
};

export const getMedicineCategories = () => fetchJson('/medicine/categories');
export const getFeaturedMedicines = () => fetchJson('/medicine/featured');

// 3. Drug Interactions
export const checkDrugInteractions = (medicines) =>
  fetchJson('/interactions/check', {
    method: 'POST',
    body: JSON.stringify({ medicines })
  });

export const getCommonInteractionPairs = () => fetchJson('/interactions/common');

// 4. AI Chatbot
export const sendChatMessage = (message, session_id = 'demo-session') =>
  fetchJson('/chat', {
    method: 'POST',
    body: JSON.stringify({ message, session_id })
  });

export const getSamplePrompts = () => fetchJson('/chat/sample-prompts');

// 5. History & Logs
export const getSearchHistory = (type = '', limit = 50) =>
  fetchJson(`/history?type=${encodeURIComponent(type)}&limit=${limit}`);

export const deleteHistoryItem = (id) =>
  fetchJson(`/history/${id}`, { method: 'DELETE' });

export const clearSearchHistory = () =>
  fetchJson('/history/clear', { method: 'POST' });
