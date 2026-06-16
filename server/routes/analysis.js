const router = require('express').Router();
const auth = require('../middleware/authMiddleware');
const { listDatasets, getDataset, deleteDataset } = require('../controllers/analysisController');

router.get('/', auth, listDatasets);
router.get('/:id', auth, getDataset);
router.delete('/:id', auth, deleteDataset);

module.exports = router;
