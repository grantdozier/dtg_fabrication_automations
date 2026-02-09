import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Box,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  MenuItem,
  TextField,
  Typography,
} from '@mui/material'
import { Add } from '@mui/icons-material'
import { api } from '../api/client'

export default function Machines() {
  const [open, setOpen] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    machine_type: 'mill',
    machine_rate_per_hr: '',
    labor_rate_per_hr: '',
    description: '',
  })
  const queryClient = useQueryClient()

  const { data: machines = [], isLoading } = useQuery({
    queryKey: ['machines'],
    queryFn: api.getMachines,
  })

  const createMutation = useMutation({
    mutationFn: api.createMachine,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['machines'] })
      setOpen(false)
      setFormData({
        name: '',
        machine_type: 'mill',
        machine_rate_per_hr: '',
        labor_rate_per_hr: '',
        description: '',
      })
    },
  })

  const handleSubmit = () => {
    createMutation.mutate({
      name: formData.name,
      machine_type: formData.machine_type,
      machine_rate_per_hr: parseFloat(formData.machine_rate_per_hr),
      labor_rate_per_hr: parseFloat(formData.labor_rate_per_hr),
      description: formData.description,
    })
  }

  if (isLoading) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Machines</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={() => setOpen(true)}>
          Add Machine
        </Button>
      </Box>

      <Grid container spacing={2}>
        {machines.map((machine) => (
          <Grid item xs={12} md={6} lg={4} key={machine.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{machine.name}</Typography>
                <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
                  {machine.machine_type.toUpperCase()}
                </Typography>
                <Typography variant="body2">
                  Machine Rate: ${machine.machine_rate_per_hr.toFixed(2)}/hr
                </Typography>
                <Typography variant="body2">
                  Labor Rate: ${machine.labor_rate_per_hr.toFixed(2)}/hr
                </Typography>
                {machine.description && (
                  <Typography variant="body2" sx={{ mt: 1 }} color="text.secondary">
                    {machine.description}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Machine</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Machine Name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              select
              label="Machine Type"
              value={formData.machine_type}
              onChange={(e) => setFormData({ ...formData, machine_type: e.target.value })}
            >
              <MenuItem value="mill">Mill</MenuItem>
              <MenuItem value="lathe">Lathe</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </TextField>
            <TextField
              label="Machine Rate ($/hr)"
              type="number"
              required
              value={formData.machine_rate_per_hr}
              onChange={(e) => setFormData({ ...formData, machine_rate_per_hr: e.target.value })}
            />
            <TextField
              label="Labor Rate ($/hr)"
              type="number"
              required
              value={formData.labor_rate_per_hr}
              onChange={(e) => setFormData({ ...formData, labor_rate_per_hr: e.target.value })}
            />
            <TextField
              label="Description"
              multiline
              rows={2}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={!formData.name || !formData.machine_rate_per_hr || !formData.labor_rate_per_hr}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
