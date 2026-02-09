import { useQuery } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material'
import { ArrowBack } from '@mui/icons-material'
import { api } from '../api/client'

export default function QuoteView() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: quote, isLoading } = useQuery({
    queryKey: ['quote', id],
    queryFn: () => api.getQuote(parseInt(id!)),
    enabled: !!id,
  })

  const { data: parts = [] } = useQuery({
    queryKey: ['parts'],
    queryFn: api.getParts,
  })

  if (isLoading) return <Typography>Loading...</Typography>
  if (!quote) return <Typography>Quote not found</Typography>

  const totalCost = quote.items.reduce((sum, item) => sum + item.unit_cost * item.quantity, 0)
  const totalPrice = quote.items.reduce((sum, item) => sum + item.unit_price * item.quantity, 0)

  return (
    <Box>
      <Button startIcon={<ArrowBack />} onClick={() => navigate('/quotes')} sx={{ mb: 2 }}>
        Back to Quotes
      </Button>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
            <Box>
              <Typography variant="h4">{quote.quote_number || `Quote #${quote.id}`}</Typography>
              <Typography color="text.secondary">Customer ID: {quote.customer_id}</Typography>
            </Box>
            <Chip label={quote.status} color="primary" />
          </Box>

          {quote.notes && (
            <>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body2">{quote.notes}</Typography>
            </>
          )}
        </CardContent>
      </Card>

      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Part Number</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell align="right">Material Cost</TableCell>
              <TableCell align="right">Machine Cost</TableCell>
              <TableCell align="right">Labor Cost</TableCell>
              <TableCell align="right">Unit Cost</TableCell>
              <TableCell align="right">Unit Price</TableCell>
              <TableCell align="right">Extended Price</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {quote.items.map((item) => {
              const part = parts.find((p) => p.id === item.part_id)
              return (
                <TableRow key={item.id}>
                  <TableCell>
                    {part?.part_number || `Part #${item.part_id}`}
                    {part?.description && (
                      <Typography variant="caption" display="block" color="text.secondary">
                        {part.description}
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell align="right">{item.quantity}</TableCell>
                  <TableCell align="right">${item.material_cost_unit.toFixed(2)}</TableCell>
                  <TableCell align="right">${item.machine_cost_unit.toFixed(2)}</TableCell>
                  <TableCell align="right">${item.labor_cost_unit.toFixed(2)}</TableCell>
                  <TableCell align="right">
                    <strong>${item.unit_cost.toFixed(2)}</strong>
                  </TableCell>
                  <TableCell align="right">
                    <strong>${item.unit_price.toFixed(2)}</strong>
                  </TableCell>
                  <TableCell align="right">
                    <strong>${(item.unit_price * item.quantity).toFixed(2)}</strong>
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </TableContainer>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Cost Summary
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography>Total Cost (At Cost):</Typography>
                <Typography fontWeight="bold">${totalCost.toFixed(2)}</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography>Total Price (With Margin):</Typography>
                <Typography fontWeight="bold" color="primary.main">
                  ${totalPrice.toFixed(2)}
                </Typography>
              </Box>
              <Divider sx={{ my: 1 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography color="success.main">Profit:</Typography>
                <Typography fontWeight="bold" color="success.main">
                  ${(totalPrice - totalCost).toFixed(2)}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
