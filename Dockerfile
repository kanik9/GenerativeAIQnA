FROM python:3.11.10-bookworm

# Set the working directory
WORKDIR /testing

# Install virtualenv and set up the virtual environment
RUN python -m pip install virtualenv && \
    python -m virtualenv venv

# Copy the application code
COPY . .

# Ensure the virtual environment is used for all subsequent commands
ENV PATH="/testing/venv/bin:$PATH"

# Install dependencies within the virtual environment
RUN python -m pip install --upgrade pip 
RUN python -m pip install --no-cache-dir -r requirements.txt --verbose
RUN pip install playwright
RUN python -m playwright install


# Expose port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
