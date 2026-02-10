import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  Chip,
  Grid,
  Typography,
} from '@mui/material'
import { Edit, Settings } from '@mui/icons-material'
import { api, Part } from '../api/client'
import PartEditor from '../components/PartEditor'

export default function Parts() {
  const [selectedPart, setSelectedPart] = useState<Part | null>(null)
  const [editorOpen, setEditorOpen] = useState(false)

  const { data: parts = [], isLoading } = useQuery({
    queryKey: ['parts'],
    queryFn: api.getParts,
  })

  const handleEdit = (part: Part) => {
    setSelectedPart(part)
    setEditorOpen(true)
  }

  const handleClose = () => {
    setEditorOpen(false)
    setSelectedPart(null)
  }

  if (isLoading) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Parts</Typography>
        <Typography variant="body2" color="text.secondary">
          Click "Edit" to modify part settings and operations
        </Typography>
      </Box>

      <Grid container spacing={2}>
        {parts.map((part) => (
          <Grid item xs={12} md={6} lg={4} key={part.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{part.part_number}</Typography>
                {part.description && (
                  <Typography color="text.secondary" sx={{ mb: 1 }}>
                    {part.description}
                  </Typography>
                )}

                <Box sx={{ my: 2 }}>
                  <Typography variant="body2" sx={{ mb: 0.5 }}>
                    Stock Weight: {part.stock_weight_lb} lb
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 0.5 }}>
                    Scrap Factor: {(part.scrap_factor * 100).toFixed(0)}%
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 0.5 }}>
                    Programming: {part.programming_time_hr} hr @ ${part.programming_rate_per_hr}/hr
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 0.5 }}>
                    FAI: {part.first_article_inspection_hr} hr
                  </Typography>
                  <Typography variant="body2">
                    Overhead: {(part.overhead_rate_pct * 100).toFixed(0)}%
                  </Typography>
                </Box>

                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    Operations ({part.operations.length}):
                  </Typography>
                  {part.operations.map((op) => (
                    <Chip
                      key={op.id}
                      label={`${op.sequence}: ${op.name}`}
                      size="small"
                      color={
                        op.operation_type === 'roughing'
                          ? 'warning'
                          : op.operation_type === 'finishing'
                          ? 'success'
                          : 'default'
                      }
                      sx={{ mr: 0.5, mb: 0.5 }}
                    />
                  ))}
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  startIcon={<Edit />}
                  onClick={() => handleEdit(part)}
                >
                  Edit Settings
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <PartEditor
        part={selectedPart}
        open={editorOpen}
        onClose={handleClose}
      />
    </Box>
  )
}
