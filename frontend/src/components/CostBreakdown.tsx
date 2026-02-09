import {
  Box,
  Card,
  CardContent,
  Divider,
  Grid,
  Typography,
} from '@mui/material'
import { QuoteBreakdown } from '../api/client'

interface Props {
  breakdown: QuoteBreakdown
  quantity: number
}

export default function CostBreakdown({ breakdown, quantity }: Props) {
  const extendedCost = breakdown.unit_cost * quantity
  const extendedPrice = breakdown.unit_price * quantity
  const profit = extendedPrice - extendedCost
  const profitMargin = ((profit / extendedCost) * 100).toFixed(1)

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Cost Breakdown
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
              Unit Costs
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography>Material:</Typography>
              <Typography>${breakdown.material_unit.toFixed(2)}</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography>Machine Time:</Typography>
              <Typography>${breakdown.machine_unit.toFixed(2)}</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography>Labor:</Typography>
              <Typography>${breakdown.labor_unit.toFixed(2)}</Typography>
            </Box>
            <Divider sx={{ my: 1 }} />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography fontWeight="bold">Unit Cost (At Cost):</Typography>
              <Typography fontWeight="bold">${breakdown.unit_cost.toFixed(2)}</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Typography fontWeight="bold" color="primary.main">
                Unit Price (With Margin):
              </Typography>
              <Typography fontWeight="bold" color="primary.main">
                ${breakdown.unit_price.toFixed(2)}
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
              Extended Totals (Qty: {quantity})
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography>Total Cost:</Typography>
              <Typography>${extendedCost.toFixed(2)}</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography color="primary.main">Total Price:</Typography>
              <Typography color="primary.main" fontWeight="bold">
                ${extendedPrice.toFixed(2)}
              </Typography>
            </Box>
            <Divider sx={{ my: 1 }} />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography color="success.main">Profit:</Typography>
              <Typography color="success.main" fontWeight="bold">
                ${profit.toFixed(2)}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Typography variant="body2" color="text.secondary">
                Margin:
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {profitMargin}%
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Box
              sx={{
                bgcolor: 'background.default',
                p: 2,
                borderRadius: 1,
              }}
            >
              <Typography variant="body2" color="text.secondary">
                <strong>Total Machine Time:</strong> {breakdown.total_time_hr.toFixed(2)} hours per
                part
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  )
}
