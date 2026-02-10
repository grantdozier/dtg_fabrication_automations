const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export interface Customer {
  id: number
  name: string
  email?: string
  phone?: string
}

export interface Material {
  id: number
  name: string
  cost_per_lb: number
  density_lb_in3: number
  description?: string
}

export interface Machine {
  id: number
  name: string
  machine_type: string
  machine_rate_per_hr: number
  labor_rate_per_hr: number
  description?: string
}

export interface Operation {
  id: number
  machine_id: number
  name: string
  sequence: number
  setup_time_hr: number
  cycle_time_hr: number
  allowance_pct: number
}

export interface Part {
  id: number
  part_number: string
  description?: string
  material_id: number
  stock_weight_lb: number
  scrap_factor: number
  operations: Operation[]
}

export interface QuoteBreakdown {
  material_unit: number
  machine_unit: number
  labor_unit: number
  unit_cost: number
  unit_price: number
  total_time_hr: number
}

export interface TimeBreakdown {
  setup_time_per_part: number
  cycle_time: number
  allowance_time: number
  tool_change_time: number
  inspection_time: number
  total_time_per_part: number
}

export interface MaterialCost {
  base: number
  scrap: number
  total: number
}

export interface CostBreakdownDetail {
  material: MaterialCost
  machine_cost: number
  labor_cost: number
  tooling_cost: number
  programming_cost: number
  inspection_cost: number
  consumables_cost: number
  overhead_cost: number
  subtotal_cost: number
  unit_cost: number
  margin_amount: number
  unit_price: number
}

export interface OperationTime {
  setup_per_part: number
  cycle: number
  allowance: number
  tool_change: number
  inspection: number
  total: number
}

export interface OperationCost {
  machine: number
  labor: number
  tooling: number
  consumables: number
  total: number
}

export interface OperationBreakdown {
  operation_name: string
  operation_type: string
  sequence: number
  time: OperationTime
  cost: OperationCost
}

export interface DetailedQuoteSummary {
  quantity: number
  unit_cost: number
  unit_price: number
  margin_pct: number
  extended_cost: number
  extended_price: number
  profit_amount: number
}

export interface PartInfo {
  part_number: string
  description: string
  material_name: string
}

export interface DetailedQuoteBreakdown {
  time_breakdown: TimeBreakdown
  cost_breakdown: CostBreakdownDetail
  operations: OperationBreakdown[]
  summary: DetailedQuoteSummary
  part_info: PartInfo
}

export interface QuoteItem {
  id: number
  part_id: number
  quantity: number
  margin_pct: number
  material_cost_unit: number
  machine_cost_unit: number
  labor_cost_unit: number
  unit_cost: number
  unit_price: number
}

export interface Quote {
  id: number
  customer_id: number
  quote_number?: string
  status: string
  notes?: string
  items: QuoteItem[]
}

async function fetchJSON<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }

  return res.json()
}

export const api = {
  // Customers
  getCustomers: () => fetchJSON<Customer[]>('/api/customers'),
  createCustomer: (data: Omit<Customer, 'id'>) =>
    fetchJSON<Customer>('/api/customers', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Materials
  getMaterials: () => fetchJSON<Material[]>('/api/materials'),
  createMaterial: (data: Omit<Material, 'id'>) =>
    fetchJSON<Material>('/api/materials', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Machines
  getMachines: () => fetchJSON<Machine[]>('/api/machines'),
  createMachine: (data: Omit<Machine, 'id'>) =>
    fetchJSON<Machine>('/api/machines', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Parts
  getParts: () => fetchJSON<Part[]>('/api/parts'),
  getPart: (id: number) => fetchJSON<Part>(`/api/parts/${id}`),
  createPart: (data: Omit<Part, 'id'>) =>
    fetchJSON<Part>('/api/parts', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Quotes
  calculateQuote: (data: { part_id: number; quantity: number; margin_pct: number }) =>
    fetchJSON<QuoteBreakdown>('/api/quotes/calculate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  calculateDetailedQuote: (data: { part_id: number; quantity: number; margin_pct: number }) =>
    fetchJSON<DetailedQuoteBreakdown>('/api/quotes/calculate-detailed', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getQuotes: () => fetchJSON<Quote[]>('/api/quotes'),
  getQuote: (id: number) => fetchJSON<Quote>(`/api/quotes/${id}`),
  createQuote: (data: {
    customer_id: number
    notes?: string
    items: { part_id: number; quantity: number; margin_pct: number }[]
  }) =>
    fetchJSON<Quote>('/api/quotes', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
}
