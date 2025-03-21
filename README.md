# MicroSense: The Micro Expression Detector

## Introduction
MicroSense: The Micro Expression Detector is a deep learning-based project designed to detect micro-expressions in video uploads. Micro-expressions are brief, involuntary facial expressions that reveal true emotions. This tool can be used for various applications, including psychological studies, security, and improving human-computer interaction.

## Features
- Detects micro-expressions in uploaded videos.
- Trained using the YOLO object detection algorithm.
- Model trained on over 10,000 examples and more than 10 different micro-expressions.
- High accuracy in detecting subtle facial expressions.
- User-friendly interface for video upload and analysis.


## Demo
### **Micro-Expression Detection in Action**
![MicroSense Demo](assets/Demo1.gif)

### **User Interface & Workflow**
![User Interface Demo](assets/user-interface-demo.gif)

## Installation
1. *Clone the repository*
    ```python
    git clone https://github.com/yogeshsumman/Micro-Expression-Detector.git
    ```
2. Make sure you have python 3.11 and pip installed in your machine.
3. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the flask application:
    ```bash
    python app.py
    ```


## Future Works
- **Real-time Processing**: Explore the implementation of real-time micro-expression detection from video streams to enhance usability in live scenarios.
- **Cross-Dataset Evaluation**: Validate the model's performance across different datasets to ensure robustness and generalizability.
- **Multi-Modal Analysis**: Integrate additional data modalities, such as audio or text, to provide a more comprehensive analysis of micro-expressions in context.
- **User Customization**: Allow users to customize detection thresholds and settings based on specific use cases or environments.
- **Mobile Deployment**: Investigate options for deploying the model on mobile devices to make micro-expression detection accessible on-the-go.

These enhancements aim to improve the utility, accessibility, and accuracy of the MicroSense project, making it a valuable resource for various fields.

## Contributing
We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or need further assistance, please contact our support team at yogeshsumman2001@gmail.com.

## Tech Stack

*Client:* HTML, CSS, JavaScript

*Server:* Flask, Sqlalchemy, Python

*Object Detection:* YOLO
