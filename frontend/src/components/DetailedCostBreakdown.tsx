import {
  Box,
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
import {
  AccessTime,
  AttachMoney,
  Build,
  Engineering,
  Inventory,
  Science,
  TrendingUp,
} from '@mui/icons-material'
import { DetailedQuoteBreakdown } from '../api/client'

interface Props {
  breakdown: DetailedQuoteBreakdown
}

export default function DetailedCostBreakdown({ breakdown }: Props) {
  const { time_breakdown, cost_breakdown, operations, summary, part_info } = breakdown

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      {/* Part Info Header */}
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box>
              <Typography variant="h5" sx={{ mb: 0.5 }}>
                {part_info.part_number}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {part_info.description}
              </Typography>
              <Chip
                label={part_info.material_name}
                size="small"
                sx={{ mt: 1 }}
                icon={<Inventory />}
              />
            </Box>
            <Box sx={{ textAlign: 'right' }}>
              <Typography variant="h4" color="primary">
                ${summary.unit_price.toFixed(2)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                per part
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Summary Section */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUp /> Quote Summary
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  Quantity
                </Typography>
                <Typography variant="h5">{summary.quantity} pcs</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, bgcolor: 'success.light' }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  Extended Price
                </Typography>
                <Typography variant="h5">${summary.extended_price.toLocaleString()}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, bgcolor: 'info.light' }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  Profit ({summary.margin_pct.toFixed(1)}% margin)
                </Typography>
                <Typography variant="h5">${summary.profit_amount.toLocaleString()}</Typography>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Time Breakdown */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <AccessTime /> Time Breakdown (per part)
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={6} sm={4}>
              <Box sx={{ textAlign: 'center', p: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Setup (amortized)
                </Typography>
                <Typography variant="h6">
                  {(time_breakdown.setup_time_per_part * 60).toFixed(1)} min
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={4}>
              <Box sx={{ textAlign: 'center', p: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Cycle Time
                </Typography>
                <Typography variant="h6">
                  {(time_breakdown.cycle_time * 60).toFixed(1)} min
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={4}>
              <Box sx={{ textAlign: 'center', p: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Allowance
                </Typography>
                <Typography variant="h6">
                  {(time_breakdown.allowance_time * 60).toFixed(1)} min
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={4}>
              <Box sx={{ textAlign: 'center', p: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Tool Changes
                </Typography>
                <Typography variant="h6">
                  {(time_breakdown.tool_change_time * 60).toFixed(1)} min
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={4}>
              <Box sx={{ textAlign: 'center', p: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Inspection
                </Typography>
                <Typography variant="h6">
                  {(time_breakdown.inspection_time * 60).toFixed(1)} min
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={4}>
              <Box
                sx={{
                  textAlign: 'center',
                  p: 1,
                  bgcolor: 'primary.light',
                  borderRadius: 1,
                }}
              >
                <Typography variant="body2" color="text.secondary">
                  Total Time
                </Typography>
                <Typography variant="h6" fontWeight="bold">
                  {(time_breakdown.total_time_per_part * 60).toFixed(1)} min
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Cost Breakdown */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <AttachMoney /> Cost Breakdown (per part)
          </Typography>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            {/* Material */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Material (stock + scrap)</Typography>
              <Typography fontWeight="medium">${cost_breakdown.material.total.toFixed(2)}</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', pl: 3, fontSize: '0.875rem' }}>
              <Typography variant="body2" color="text.secondary">
                Stock: {cost_breakdown.material.base.toFixed(2)} + Scrap:{' '}
                {cost_breakdown.material.scrap.toFixed(2)}
              </Typography>
            </Box>

            <Divider sx={{ my: 1 }} />

            {/* Time-based costs */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Machine Time</Typography>
              <Typography fontWeight="medium">${cost_breakdown.machine_cost.toFixed(2)}</Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Labor</Typography>
              <Typography fontWeight="medium">${cost_breakdown.labor_cost.toFixed(2)}</Typography>
            </Box>

            <Divider sx={{ my: 1 }} />

            {/* Additional costs */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Tooling (wear & replacement)</Typography>
              <Typography fontWeight="medium">${cost_breakdown.tooling_cost.toFixed(2)}</Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Programming (amortized)</Typography>
              <Typography fontWeight="medium">${cost_breakdown.programming_cost.toFixed(2)}</Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Inspection (FAI + in-process)</Typography>
              <Typography fontWeight="medium">${cost_breakdown.inspection_cost.toFixed(2)}</Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Consumables (coolant, etc.)</Typography>
              <Typography fontWeight="medium">${cost_breakdown.consumables_cost.toFixed(2)}</Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography>Overhead</Typography>
              <Typography fontWeight="medium">${cost_breakdown.overhead_cost.toFixed(2)}</Typography>
            </Box>

            <Divider sx={{ my: 1 }} />

            {/* Totals */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography fontWeight="bold">Subtotal (at cost)</Typography>
              <Typography fontWeight="bold">${cost_breakdown.subtotal_cost.toFixed(2)}</Typography>
            </Box>

            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                py: 1,
                bgcolor: 'warning.light',
                px: 2,
                borderRadius: 1,
              }}
            >
              <Typography fontWeight="bold">Unit Cost</Typography>
              <Typography fontWeight="bold" variant="h6">
                ${cost_breakdown.unit_cost.toFixed(2)}
              </Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
              <Typography color="success.main">
                Margin ({summary.margin_pct.toFixed(1)}%)
              </Typography>
              <Typography color="success.main" fontWeight="medium">
                +${cost_breakdown.margin_amount.toFixed(2)}
              </Typography>
            </Box>

            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                py: 1,
                bgcolor: 'success.light',
                px: 2,
                borderRadius: 1,
                mt: 1,
              }}
            >
              <Typography fontWeight="bold">Unit Price</Typography>
              <Typography fontWeight="bold" variant="h6" color="success.dark">
                ${cost_breakdown.unit_price.toFixed(2)}
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Operations Breakdown */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Build /> Operations Breakdown
          </Typography>

          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Operation</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell align="right">Time (min)</TableCell>
                  <TableCell align="right">Machine</TableCell>
                  <TableCell align="right">Labor</TableCell>
                  <TableCell align="right">Tooling</TableCell>
                  <TableCell align="right">Total Cost</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {operations.map((op) => (
                  <TableRow key={op.sequence}>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {op.operation_name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={op.operation_type}
                        size="small"
                        color={
                          op.operation_type === 'roughing'
                            ? 'warning'
                            : op.operation_type === 'finishing'
                            ? 'success'
                            : 'default'
                        }
                      />
                    </TableCell>
                    <TableCell align="right">
                      {(op.time.total * 60).toFixed(1)}
                    </TableCell>
                    <TableCell align="right">${op.cost.machine.toFixed(2)}</TableCell>
                    <TableCell align="right">${op.cost.labor.toFixed(2)}</TableCell>
                    <TableCell align="right">${op.cost.tooling.toFixed(2)}</TableCell>
                    <TableCell align="right">
                      <Typography fontWeight="bold">${op.cost.total.toFixed(2)}</Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Extended Totals */}
      <Card sx={{ bgcolor: 'primary.light' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Engineering /> Extended Totals (Qty: {summary.quantity})
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Total Cost
                </Typography>
                <Typography variant="h5">${summary.extended_cost.toLocaleString()}</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Total Price
                </Typography>
                <Typography variant="h5" color="primary">
                  ${summary.extended_price.toLocaleString()}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Profit
                </Typography>
                <Typography variant="h5" color="success.main">
                  ${summary.profit_amount.toLocaleString()}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  )
}
