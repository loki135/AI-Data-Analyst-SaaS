require('dotenv').config();
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

const mongoUri = process.env.MONGO_URI || process.env.MONGO_URL || process.env.MONGO_CONN || process.env.MONGO_SRV_URI;
if (!mongoUri) {
  console.error('Missing MONGO_URI in .env');
  process.exit(1);
}

async function run() {
  await mongoose.connect(mongoUri);
  console.log('Connected to MongoDB');

  const email = 'test+lokesh@example.com';
  let user = await User.findOne({ email });
  if (!user) {
    user = new User({ name: 'Lokesh Test', email, password: 'password123' });
    await user.save();
    console.log('Created test user:', email);
  } else {
    console.log('Test user already exists:', email);
  }

  const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '7d' });
  console.log('\nTEST_JWT=' + token + '\n');

  await mongoose.disconnect();
  process.exit(0);
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
