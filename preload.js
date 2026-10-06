const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(app.getPath('userData'), 'imose-crm-data.json');

const defaultData = {
  users: [
    { id: 1, username: 'admin', password: 'admin123', role: 'admin' }
  ],
  customers: [
    { id: 1, name: 'John Smith', phone: '08034567890', email: 'john@example.com', address: 'Lagos' },
    { id: 2, name: 'Ada Okafor', phone: '09011223344', email: 'ada@example.com', address: 'Abuja' }
  ],
  repairTickets: [
    { id: 1, customerId: 1, customerName: 'John Smith', deviceType: 'iPhone 13', model: 'A2482', issue: 'Screen cracked', status: 'Pending', createdAt: '2026-10-06' },
    { id: 2, customerId: 2, customerName: 'Ada Okafor', deviceType: 'Samsung S23', model: 'SM-S911B', issue: 'Battery replacement', status: 'In Progress', createdAt: '2026-10-06' }
  ],
  inventory: [
    { id: 1, partName: 'iPhone Screen', code: 'IPH-SCR-01', quantity: 8, unitPrice: 22000, supplier: 'Global Fix Supplies' },
    { id: 2, partName: 'Samsung Battery', code: 'SAM-BAT-02', quantity: 6, unitPrice: 18000, supplier: 'Mobile Parts Ltd' }
  ],
  invoices: [
    { id: 1, ticketId: 1, customerId: 1, customerName: 'John Smith', amount: 45000, status: 'Paid', method: 'Cash', createdAt: '2026-10-06' },
    { id: 2, ticketId: 2, customerId: 2, customerName: 'Ada Okafor', amount: 65000, status: 'Unpaid', method: 'Transfer', createdAt: '2026-10-06' }
  ]
};

function ensureDataFile() {
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(defaultData, null, 2));
  }

  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw);
  } catch (error) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(defaultData, null, 2));
    return JSON.parse(JSON.stringify(defaultData));
  }
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 1100,
    backgroundColor: '#f6f7fb',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipcMain.handle('login', (_, username, password) => {
  const data = ensureDataFile();
  const user = data.users.find(
    (entry) => entry.username === username && entry.password === password
  );

  if (!user) {
    return null;
  }

  return {
    id: user.id,
    username: user.username,
    role: user.role || 'admin'
  };
});

ipcMain.handle('getAppData', () => {
  return ensureDataFile();
});

ipcMain.handle('addCustomer', (_, customer) => {
  const data = ensureDataFile();
  const id = data.customers.length ? Math.max(...data.customers.map((item) => item.id)) + 1 : 1;

  data.customers.push({
    id,
    name: customer.name,
    phone: customer.phone,
    email: customer.email || '',
    address: customer.address || ''
  });

  saveData(data);
  return data;
});

ipcMain.handle('deleteCustomer', (_, customerId) => {
  const data = ensureDataFile();
  data.customers = data.customers.filter((customer) => customer.id !== Number(customerId));
  data.repairTickets = data.repairTickets.filter((ticket) => ticket.customerId !== Number(customerId));
  data.invoices = data.invoices.filter((invoice) => invoice.customerId !== Number(customerId));
  saveData(data);
  return data;
});

ipcMain.handle('addRepairTicket', (_, ticket) => {
  const data = ensureDataFile();
  const customer = data.customers.find((entry) => entry.id === Number(ticket.customerId));
  const id = data.repairTickets.length ? Math.max(...data.repairTickets.map((item) => item.id)) + 1 : 1;

  data.repairTickets.push({
    id,
    customerId: Number(ticket.customerId),
    customerName: customer ? customer.name : 'Unknown',
    deviceType: ticket.deviceType,
    model: ticket.model || '',
    issue: ticket.issue || '',
    status: 'Pending',
    createdAt: new Date().toISOString().slice(0, 10)
  });

  saveData(data);
  return data;
});

ipcMain.handle('updateTicketStatus', (_, ticketId, status) => {
  const data = ensureDataFile();
  const ticket = data.repairTickets.find((entry) => entry.id === Number(ticketId));

  if (ticket) {
    ticket.status = status;
  }

  saveData(data);
  return data;
});

ipcMain.handle('addPart', (_, part) => {
  const data = ensureDataFile();
  const id = data.inventory.length ? Math.max(...data.inventory.map((item) => item.id)) + 1 : 1;

  data.inventory.push({
    id,
    partName: part.partName,
    code: part.code || '',
    quantity: Number(part.quantity || 0),
    unitPrice: Number(part.unitPrice || 0),
    supplier: part.supplier || ''
  });

  saveData(data);
  return data;
});

ipcMain.handle('deletePart', (_, partId) => {
  const data = ensureDataFile();
  data.inventory = data.inventory.filter((item) => item.id !== Number(partId));
  saveData(data);
  return data;
});

ipcMain.handle('addInvoice', (_, invoice) => {
  const data = ensureDataFile();
  const customer = data.customers.find((entry) => entry.id === Number(invoice.customerId));
  const ticket = data.repairTickets.find((entry) => entry.id === Number(invoice.ticketId));
  const id = data.invoices.length ? Math.max(...data.invoices.map((item) => item.id)) + 1 : 1;

  data.invoices.push({
    id,
    ticketId: Number(invoice.ticketId),
    customerId: Number(invoice.customerId),
    customerName: customer ? customer.name : ticket ? ticket.customerName : 'Unknown',
    amount: Number(invoice.amount || 0),
    status: 'Unpaid',
    method: invoice.method || 'Cash',
    createdAt: new Date().toISOString().slice(0, 10)
  });

  saveData(data);
  return data;
});

ipcMain.handle('markInvoicePaid', (_, invoiceId) => {
  const data = ensureDataFile();
  const invoice = data.invoices.find((entry) => entry.id === Number(invoiceId));

  if (invoice) {
    invoice.status = 'Paid';
  }

  saveData(data);
  return data;
});
