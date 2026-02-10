import { useState } from 'react'
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  TextField,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  MenuItem,
  IconButton,
} from '@mui/material'
import { ExpandMore, Delete, Add } from '@mui/icons-material'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { api, Part, Machine } from '../api/client'

interface Props {
  part: Part | null
  open: boolean
  onClose: () => void
}

const OPERATION_TYPES = [
  { value: 'roughing', label: 'Roughing' },
  { value: 'finishing', label: 'Finishing' },
  { value: 'machining', label: 'Machining' },
  { value: 'deburr', label: 'Deburr' },
  { value: 'inspection', label: 'Inspection' },
]

export default function PartEditor({ part, open, onClose }: Props) {
  const queryClient = useQueryClient()

  // Form state for Part fields
  const [partData, setPartData] = useState({
    stock_weight_lb: part?.stock_weight_lb || 1.0,
    scrap_factor: part?.scrap_factor || 0.05,
    programming_time_hr: part?.programming_time_hr || 0.0,
    programming_rate_per_hr: part?.programming_rate_per_hr || 75.0,
    first_article_inspection_hr: part?.first_article_inspection_hr || 0.0,
    overhead_rate_pct: part?.overhead_rate_pct || 1.5,
  })

  // Form state for Operations
  const [operations, setOperations] = useState(
    part?.operations || []
  )

  const { data: machines = [] } = useQuery({
    queryKey: ['machines'],
    queryFn: api.getMachines,
  })

  const updateMutation = useMutation({
    mutationFn: async (data: any) => {
      if (!part) return
      return api.updatePart(part.id, data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parts'] })
      onClose()
    },
  })

  const updateOperationMutation = useMutation({
    mutationFn: ({ partId, opId, data }: any) => {
      return api.updateOperation(partId, opId, data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parts'] })
    },
  })

  const handleSave = () => {
    if (!part) return

    // Update part
    updateMutation.mutate(partData)

    // Update all operations
    operations.forEach((op: any) => {
      updateOperationMutation.mutate({
        partId: part.id,
        opId: op.id,
        data: {
          machine_id: op.machine_id,
          name: op.name,
          sequence: op.sequence,
          setup_time_hr: op.setup_time_hr,
          cycle_time_hr: op.cycle_time_hr,
          allowance_pct: op.allowance_pct,
          operation_type: op.operation_type,
          tool_cost_per_part: op.tool_cost_per_part,
          tool_change_time_min: op.tool_change_time_min,
          inspection_time_min: op.inspection_time_min,
          consumables_cost_per_part: op.consumables_cost_per_part,
        },
      })
    })
  }

  const updatePartField = (field: string, value: any) => {
    setPartData((prev) => ({ ...prev, [field]: value }))
  }

  const updateOperationField = (index: number, field: string, value: any) => {
    setOperations((prev: any) =>
      prev.map((op: any, i: number) =>
        i === index ? { ...op, [field]: value } : op
      )
    )
  }

  if (!part) return null

  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>
        Edit Part: {part.part_number}
        <Typography variant="body2" color="text.secondary">
          {part.description}
        </Typography>
      </DialogTitle>

      <DialogContent dividers>
        {/* Part-Level Settings */}
        <Typography variant="h6" sx={{ mb: 2 }}>
          Part Settings
        </Typography>

        <Grid container spacing={2} sx={{ mb: 4 }}>
          <Grid item xs={12} md={6}>
            <TextField
              label="Stock Weight (lb)"
              type="number"
              fullWidth
              value={partData.stock_weight_lb}
              onChange={(e) => updatePartField('stock_weight_lb', parseFloat(e.target.value))}
              inputProps={{ step: 0.1, min: 0 }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Scrap Factor (%)"
              type="number"
              fullWidth
              value={partData.scrap_factor * 100}
              onChange={(e) => updatePartField('scrap_factor', parseFloat(e.target.value) / 100)}
              inputProps={{ step: 1, min: 0, max: 100 }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Programming Time (hours)"
              type="number"
              fullWidth
              value={partData.programming_time_hr}
              onChange={(e) => updatePartField('programming_time_hr', parseFloat(e.target.value))}
              inputProps={{ step: 0.5, min: 0 }}
              helperText="CAM/programming time for this part"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Programming Rate ($/hr)"
              type="number"
              fullWidth
              value={partData.programming_rate_per_hr}
              onChange={(e) => updatePartField('programming_rate_per_hr', parseFloat(e.target.value))}
              inputProps={{ step: 5, min: 0 }}
              helperText="Hourly rate for programming labor"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="First Article Inspection (hours)"
              type="number"
              fullWidth
              value={partData.first_article_inspection_hr}
              onChange={(e) => updatePartField('first_article_inspection_hr', parseFloat(e.target.value))}
              inputProps={{ step: 0.25, min: 0 }}
              helperText="One-time FAI time (amortized)"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Overhead Rate (%)"
              type="number"
              fullWidth
              value={partData.overhead_rate_pct * 100}
              onChange={(e) => updatePartField('overhead_rate_pct', parseFloat(e.target.value) / 100)}
              inputProps={{ step: 10, min: 0 }}
              helperText="Shop overhead multiplier (150% = 1.5)"
            />
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        {/* Operations */}
        <Typography variant="h6" sx={{ mb: 2 }}>
          Operations
        </Typography>

        {operations.map((op: any, index: number) => (
          <Accordion key={op.id} defaultExpanded={index === 0}>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography>
                {op.sequence} - {op.name} ({op.operation_type})
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <TextField
                    label="Operation Name"
                    fullWidth
                    value={op.name}
                    onChange={(e) => updateOperationField(index, 'name', e.target.value)}
                  />
                </Grid>

                <Grid item xs={12} md={3}>
                  <TextField
                    label="Sequence"
                    type="number"
                    fullWidth
                    value={op.sequence}
                    onChange={(e) => updateOperationField(index, 'sequence', parseInt(e.target.value))}
                    inputProps={{ step: 10 }}
                  />
                </Grid>

                <Grid item xs={12} md={3}>
                  <TextField
                    select
                    label="Operation Type"
                    fullWidth
                    value={op.operation_type}
                    onChange={(e) => updateOperationField(index, 'operation_type', e.target.value)}
                  >
                    {OPERATION_TYPES.map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        {type.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 2, mb: 1 }}>
                    Time Settings
                  </Typography>
                </Grid>

                <Grid item xs={12} md={4}>
                  <TextField
                    label="Setup Time (hours)"
                    type="number"
                    fullWidth
                    value={op.setup_time_hr}
                    onChange={(e) => updateOperationField(index, 'setup_time_hr', parseFloat(e.target.value))}
                    inputProps={{ step: 0.25, min: 0 }}
                  />
                </Grid>

                <Grid item xs={12} md={4}>
                  <TextField
                    label="Cycle Time (hours)"
                    type="number"
                    fullWidth
                    value={op.cycle_time_hr}
                    onChange={(e) => updateOperationField(index, 'cycle_time_hr', parseFloat(e.target.value))}
                    inputProps={{ step: 0.05, min: 0 }}
                  />
                </Grid>

                <Grid item xs={12} md={4}>
                  <TextField
                    label="Allowance (%)"
                    type="number"
                    fullWidth
                    value={op.allowance_pct * 100}
                    onChange={(e) => updateOperationField(index, 'allowance_pct', parseFloat(e.target.value) / 100)}
                    inputProps={{ step: 1, min: 0 }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    label="Tool Change Time (minutes)"
                    type="number"
                    fullWidth
                    value={op.tool_change_time_min}
                    onChange={(e) => updateOperationField(index, 'tool_change_time_min', parseFloat(e.target.value))}
                    inputProps={{ step: 0.5, min: 0 }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    label="Inspection Time (minutes)"
                    type="number"
                    fullWidth
                    value={op.inspection_time_min}
                    onChange={(e) => updateOperationField(index, 'inspection_time_min', parseFloat(e.target.value))}
                    inputProps={{ step: 0.5, min: 0 }}
                  />
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 2, mb: 1 }}>
                    Cost Settings
                  </Typography>
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    label="Tool Cost per Part ($)"
                    type="number"
                    fullWidth
                    value={op.tool_cost_per_part}
                    onChange={(e) => updateOperationField(index, 'tool_cost_per_part', parseFloat(e.target.value))}
                    inputProps={{ step: 0.05, min: 0 }}
                    helperText="Tool wear allocation per part"
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    label="Consumables Cost per Part ($)"
                    type="number"
                    fullWidth
                    value={op.consumables_cost_per_part}
                    onChange={(e) => updateOperationField(index, 'consumables_cost_per_part', parseFloat(e.target.value))}
                    inputProps={{ step: 0.05, min: 0 }}
                    helperText="Coolant, abrasives, etc."
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        ))}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={updateMutation.isPending}
        >
          Save Changes
        </Button>
      </DialogActions>
    </Dialog>
  )
}
