const router = require('express').Router();
const multer = require('multer');
const auth = require('../middleware/authMiddleware');
const { uploadCSV } = require('../controllers/uploadController');

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'text/csv' || file.originalname.endsWith('.csv')) {
      cb(null, true);
    } else {
      cb(new Error('Only CSV files are allowed'));
    }
  },
});

router.post('/', auth, upload.single('file'), uploadCSV);

module.exports = router;
