import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  Typography,
} from '@mui/material'
import { Add } from '@mui/icons-material'
import { api } from '../api/client'

export default function Quotes() {
  const navigate = useNavigate()

  const { data: quotes = [], isLoading } = useQuery({
    queryKey: ['quotes'],
    queryFn: api.getQuotes,
  })

  if (isLoading) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Quotes</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => navigate('/quotes/new')}
        >
          New Quote
        </Button>
      </Box>

      <Grid container spacing={2}>
        {quotes.map((quote) => (
          <Grid item xs={12} md={6} lg={4} key={quote.id}>
            <Card
              sx={{ cursor: 'pointer', '&:hover': { boxShadow: 4 } }}
              onClick={() => navigate(`/quotes/${quote.id}`)}
            >
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="h6">{quote.quote_number || `Quote #${quote.id}`}</Typography>
                  <Chip label={quote.status} size="small" color="primary" />
                </Box>
                <Typography color="text.secondary" sx={{ mb: 1 }}>
                  Customer ID: {quote.customer_id}
                </Typography>
                <Typography variant="body2">
                  {quote.items.length} item(s)
                </Typography>
                {quote.notes && (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 1, fontStyle: 'italic' }}
                  >
                    {quote.notes.substring(0, 60)}
                    {quote.notes.length > 60 && '...'}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {quotes.length === 0 && (
        <Card>
          <CardContent>
            <Typography align="center" color="text.secondary">
              No quotes yet. Create your first quote!
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
