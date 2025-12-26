-- Create table for storing PPT file metadata
CREATE TABLE IF NOT EXISTS codestorm_ppt_files (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(255) NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    original_name VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    s3_url TEXT NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registration_id INTEGER REFERENCES codestorm_registrations(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_team_name ON codestorm_ppt_files(team_name);
CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_s3_key ON codestorm_ppt_files(s3_key);
CREATE INDEX IF NOT EXISTS idx_codestorm_ppt_registration_id ON codestorm_ppt_files(registration_id);

-- Add PPT file reference to registrations table
ALTER TABLE codestorm_registrations 
ADD COLUMN IF NOT EXISTS ppt_file_id INTEGER REFERENCES codestorm_ppt_files(id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS update_codestorm_ppt_updated_at ON codestorm_ppt_files;
CREATE TRIGGER update_codestorm_ppt_updated_at
    BEFORE UPDATE ON codestorm_ppt_files
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();