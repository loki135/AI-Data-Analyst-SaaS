const router = require('express').Router();
const auth = require('../middleware/authMiddleware');
const { askQuestion, suggestChart } = require('../controllers/aiController');

router.post('/ask', auth, askQuestion);
router.post('/suggest-chart', auth, suggestChart);

module.exports = router;
