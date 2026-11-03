"""
Services for the barcode application.
"""
import base64
from io import BytesIO
import qrcode
from django.core.files.base import ContentFile
from .models import Barcode, BarcodeTemplate


class BarcodeService:
    """
    Service for barcode generation and operations.
    """
    
    def __init__(self):
        pass
    
    def generate_barcode(self, data, symbology='code128', width=200, height=50, show_text=True):
        """
        Generate a barcode image.
        """
        try:
            # For QR codes
            if symbology.lower() == 'qr_code':
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                img = img.convert('RGB')
                
                # Resize
                img = img.resize((width, height), resample=0)
                
                # Convert to base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                return f"data:image/png;base64,{img_str}"
            
            # For other symbologies, we would use a library like python-barcode
            # For now, we'll just return a placeholder
            # In a real implementation, we would use:
            # import barcode
            # from barcode.writer import ImageWriter
            # barcode_class = barcode.get_barcode_class(symbology)
            # barcode_obj = barcode_class(data, writer=ImageWriter())
            # buffered = BytesIO()
            # barcode_obj.write(buffered, options={'width': width, 'height': height})
            # img_str = base64.b64encode(buffered.getvalue()).decode()
            # return f"data:image/png;base64,{img_str}"
            
            # For now, return a simple base64 encoded placeholder
            return self.generate_placeholder_barcode(data, width, height)
            
        except Exception as e:
            return None
    
    def generate_placeholder_barcode(self, data, width, height):
        """
        Generate a placeholder barcode image.
        """
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a blank image
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw barcode-like lines
        line_width = 2
        line_height = height - 20
        x = 10
        
        for char in data[:20]:
            # Alternate between black and white lines
            color = 'black' if ord(char) % 2 == 0 else 'white'
            draw.rectangle([x, 10, x + line_width, 10 + line_height], fill=color)
            x += line_width + 1
        
        # Draw text
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, height - 18), data[:20], fill='black', font=font)
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def create_barcode(self, data, **kwargs):
        """
        Create a new barcode record.
        """
        barcode = Barcode.objects.create(
            data=data,
            symbology=kwargs.get('symbology', 'code128'),
            width=kwargs.get('width', 200),
            height=kwargs.get('height', 50),
            show_text=kwargs.get('show_text', True),
            text_position=kwargs.get('text_position', 'bottom'),
            related_entity_type=kwargs.get('related_entity_type'),
            related_entity_id=kwargs.get('related_entity_id'),
            organization=kwargs.get('organization'),
            branch=kwargs.get('branch'),
            created_by=kwargs.get('created_by'),
            is_active=kwargs.get('is_active', True)
        )
        
        return self.get_barcode_data(barcode)
    
    def get_barcode_data(self, barcode):
        """
        Get barcode data for API responses.
        """
        return {
            'id': str(barcode.id),
            'data': barcode.data,
            'symbology': barcode.symbology,
            'symbology_display': barcode.get_symbology_display(),
            'width': barcode.width,
            'height': barcode.height,
            'show_text': barcode.show_text,
            'text_position': barcode.text_position,
            'related_entity_type': barcode.related_entity_type,
            'related_entity_id': str(barcode.related_entity_id) if barcode.related_entity_id else None,
            'organization': {
                'id': str(barcode.organization.id),
                'name': barcode.organization.name,
            } if barcode.organization else None,
            'branch': {
                'id': str(barcode.branch.id),
                'name': barcode.branch.name,
            } if barcode.branch else None,
            'created_by': {
                'id': str(barcode.created_by.id) if barcode.created_by else None,
                'email': barcode.created_by.email if barcode.created_by else None,
            } if barcode.created_by else None,
            'is_active': barcode.is_active,
            'image_url': barcode.get_image_url(),
            'created_at': barcode.created_at.isoformat(),
        }
    
    def create_barcode_template(self, data):
        """
        Create a new barcode template.
        """
        template = BarcodeTemplate.objects.create(
            name=data.get('name'),
            code=data.get('code'),
            symbology=data.get('symbology', 'code128'),
            width=data.get('width', 200),
            height=data.get('height', 50),
            show_text=data.get('show_text', True),
            text_position=data.get('text_position', 'bottom'),
            organization=data.get('organization'),
            created_by=data.get('created_by'),
            is_active=data.get('is_active', True)
        )
        
        return self.get_barcode_template_data(template)
    
    def get_barcode_template_data(self, template):
        """
        Get barcode template data for API responses.
        """
        return {
            'id': str(template.id),
            'name': template.name,
            'code': template.code,
            'symbology': template.symbology,
            'symbology_display': template.get_symbology_display(),
            'width': template.width,
            'height': template.height,
            'show_text': template.show_text,
            'text_position': template.text_position,
            'organization': {
                'id': str(template.organization.id),
                'name': template.organization.name,
            },
            'created_by': {
                'id': str(template.created_by.id) if template.created_by else None,
                'email': template.created_by.email if template.created_by else None,
            } if template.created_by else None,
            'is_active': template.is_active,
            'created_at': template.created_at.isoformat(),
            'updated_at': template.updated_at.isoformat(),
        }
