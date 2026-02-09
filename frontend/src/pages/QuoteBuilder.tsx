import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
  Alert,
} from '@mui/material'
import { Save } from '@mui/icons-material'
import { api, QuoteBreakdown } from '../api/client'
import CostBreakdown from '../components/CostBreakdown'

export default function QuoteBuilder() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [customerId, setCustomerId] = useState<number | ''>('')
  const [partId, setPartId] = useState<number | ''>('')
  const [quantity, setQuantity] = useState(100)
  const [marginPct, setMarginPct] = useState(0.15)
  const [notes, setNotes] = useState('')
  const [breakdown, setBreakdown] = useState<QuoteBreakdown | null>(null)
  const [error, setError] = useState('')

  const { data: customers = [] } = useQuery({
    queryKey: ['customers'],
    queryFn: api.getCustomers,
  })

  const { data: parts = [] } = useQuery({
    queryKey: ['parts'],
    queryFn: api.getParts,
  })

  const createMutation = useMutation({
    mutationFn: api.createQuote,
    onSuccess: (quote) => {
      queryClient.invalidateQueries({ queryKey: ['quotes'] })
      navigate(`/quotes/${quote.id}`)
    },
    onError: (err: Error) => {
      setError(err.message)
    },
  })

  // Real-time calculation
  useEffect(() => {
    if (partId && quantity > 0) {
      api
        .calculateQuote({
          part_id: partId as number,
          quantity,
          margin_pct: marginPct,
        })
        .then(setBreakdown)
        .catch(() => setBreakdown(null))
    } else {
      setBreakdown(null)
    }
  }, [partId, quantity, marginPct])

  const handleSave = () => {
    if (!customerId || !partId) {
      setError('Please select customer and part')
      return
    }

    createMutation.mutate({
      customer_id: customerId as number,
      notes,
      items: [
        {
          part_id: partId as number,
          quantity,
          margin_pct: marginPct,
        },
      ],
    })
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        New Quote
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Quote Details
          </Typography>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Customer</InputLabel>
              <Select
                value={customerId}
                label="Customer"
                onChange={(e) => setCustomerId(e.target.value as number)}
              >
                {customers.map((c) => (
                  <MenuItem key={c.id} value={c.id}>
                    {c.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Part</InputLabel>
              <Select
                value={partId}
                label="Part"
                onChange={(e) => setPartId(e.target.value as number)}
              >
                {parts.map((p) => (
                  <MenuItem key={p.id} value={p.id}>
                    {p.part_number} - {p.description}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Quantity"
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
              inputProps={{ min: 1 }}
            />

            <TextField
              label="Margin %"
              type="number"
              value={marginPct * 100}
              onChange={(e) => setMarginPct(parseFloat(e.target.value) / 100 || 0.15)}
              inputProps={{ min: 0, max: 100, step: 1 }}
              helperText="Profit margin percentage"
            />

            <TextField
              label="Notes"
              multiline
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </Box>
        </CardContent>
      </Card>

      {breakdown && <CostBreakdown breakdown={breakdown} quantity={quantity} />}

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 3 }}>
        <Button variant="outlined" onClick={() => navigate('/quotes')}>
          Cancel
        </Button>
        <Button
          variant="contained"
          startIcon={<Save />}
          onClick={handleSave}
          disabled={!customerId || !partId || createMutation.isPending}
        >
          Save Quote
        </Button>
      </Box>
    </Box>
  )
}
