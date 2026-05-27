const ADMIN_PASSWORD = 'masha2024';

let isLoggedIn = false;
let currentData = null;
let editingItem = null;
let editingType = null;

document.addEventListener('DOMContentLoaded', () => {
  const saved = sessionStorage.getItem('admin_auth');
  if (saved === 'true') {
    isLoggedIn = true;
    showAdminPanel();
  }

  document.getElementById('login-form').addEventListener('submit', handleLogin);
});

function handleLogin(e) {
  e.preventDefault();
  const pwd = document.getElementById('admin-password').value;
  if (pwd === ADMIN_PASSWORD) {
    isLoggedIn = true;
    sessionStorage.setItem('admin_auth', 'true');
    showAdminPanel();
  } else {
    showToast('Wrong password!', 'error');
  }
}

async function showAdminPanel() {
  document.getElementById('login-section').style.display = 'none';
  document.getElementById('admin-panel').classList.add('active');
  await loadAdminData();
}

async function loadAdminData() {
  try {
    const res = await fetch('data.json?' + Date.now());
    currentData = await res.json();
    renderAdminTable('bots');
    renderAdminTable('channels');
  } catch (err) {
    showToast('Failed to load data', 'error');
  }
}

function renderAdminTable(type) {
  const items = currentData[type];
  const tbody = document.getElementById(`${type}-tbody`);

  if (!items.length) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:28px;">No ${type} added yet</td></tr>`;
    return;
  }

  tbody.innerHTML = items.map(item => `
    <tr>
      <td>${item.icon} ${escapeHtml(item.name)}</td>
      <td>@${escapeHtml(item.username)}</td>
      <td>${escapeHtml(item.category || '-')}</td>
      <td>
        <span class="card-status ${item.is_active ? 'active' : 'inactive'}">
          ${item.is_active ? 'Active' : 'Inactive'}
        </span>
      </td>
      <td>
        <div class="table-actions">
          <button class="btn btn-secondary btn-sm" onclick="openEditModal('${type}', ${item.id})">Edit</button>
          <button class="btn btn-danger btn-sm" onclick="deleteItem('${type}', ${item.id})">Delete</button>
        </div>
      </td>
    </tr>
  `).join('');
}

function openAddModal(type) {
  editingItem = null;
  editingType = type;
  document.getElementById('modal-title').textContent = `Add ${type === 'bots' ? 'Bot' : 'Channel'}`;
  document.getElementById('item-name').value = '';
  document.getElementById('item-username').value = '';
  document.getElementById('item-description').value = '';
  document.getElementById('item-icon').value = type === 'bots' ? '🤖' : '📢';
  document.getElementById('item-category').value = '';
  document.getElementById('item-active').checked = true;
  document.getElementById('modal-overlay').classList.add('active');
}

function openEditModal(type, id) {
  editingType = type;
  editingItem = currentData[type].find(i => i.id === id);
  if (!editingItem) return;

  document.getElementById('modal-title').textContent = `Edit ${type === 'bots' ? 'Bot' : 'Channel'}`;
  document.getElementById('item-name').value = editingItem.name;
  document.getElementById('item-username').value = editingItem.username;
  document.getElementById('item-description').value = editingItem.description;
  document.getElementById('item-icon').value = editingItem.icon;
  document.getElementById('item-category').value = editingItem.category || '';
  document.getElementById('item-active').checked = editingItem.is_active;
  document.getElementById('modal-overlay').classList.add('active');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('active');
  editingItem = null;
  editingType = null;
}

function saveItem() {
  const name = document.getElementById('item-name').value.trim();
  const username = document.getElementById('item-username').value.trim().replace('@', '');
  const description = document.getElementById('item-description').value.trim();
  const icon = document.getElementById('item-icon').value.trim();
  const category = document.getElementById('item-category').value.trim();
  const isActive = document.getElementById('item-active').checked;

  if (!name || !username) {
    showToast('Name and username are required!', 'error');
    return;
  }

  if (editingItem) {
    editingItem.name = name;
    editingItem.username = username;
    editingItem.description = description;
    editingItem.icon = icon;
    editingItem.category = category;
    editingItem.is_active = isActive;
    showToast('Item updated!', 'success');
  } else {
    const maxId = currentData[editingType].reduce((max, i) => Math.max(max, i.id), 0);
    currentData[editingType].push({
      id: maxId + 1,
      name,
      username,
      description,
      icon,
      category,
      is_active: isActive
    });
    showToast('Item added!', 'success');
  }

  renderAdminTable(editingType);
  closeModal();
  showExportData();
}

function deleteItem(type, id) {
  if (!confirm('Are you sure you want to delete this item?')) return;
  currentData[type] = currentData[type].filter(i => i.id !== id);
  renderAdminTable(type);
  showToast('Item deleted!', 'success');
  showExportData();
}

function showExportData() {
  const exportArea = document.getElementById('export-section');
  const exportJson = document.getElementById('export-json');
  exportArea.style.display = 'block';
  exportJson.value = JSON.stringify(currentData, null, 2);
}

function copyExportData() {
  const exportJson = document.getElementById('export-json');
  exportJson.select();
  document.execCommand('copy');
  showToast('JSON copied to clipboard!', 'success');
}

function downloadExportData() {
  const json = JSON.stringify(currentData, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'data.json';
  a.click();
  URL.revokeObjectURL(url);
  showToast('File downloaded! Replace docs/data.json in your repo.', 'success');
}

function showToast(message, type = 'success') {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `${type === 'success' ? '✓' : '✕'} ${message}`;
  document.body.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function logout() {
  sessionStorage.removeItem('admin_auth');
  location.reload();
}
