#!/usr/bin/env python3
"""
🎬 Video Terminal Tool 🎬
A cool command-line interface for video processing
Features: Resize videos and split videos by duration
"""

import os
import sys
import ffmpeg
from pathlib import Path
import time

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.align import Align
    from rich.box import ROUNDED, DOUBLE, HEAVY
except ImportError:
    print("❌ Error: 'rich' package not found!")
    print("💡 Install it with: pip install rich")
    sys.exit(1)

# Create console instance
console = Console()

def print_banner():
    """Print a cool banner using rich"""
    title = Text("🎬 VIDEO TERMINAL TOOL 🎬", style="bold magenta")
    subtitle = Text("Resize & Split Videos Like a Pro!", style="cyan")
    
    # Create the main panel
    banner_content = Align.center(Text.assemble(title, "\n", subtitle))
    
    banner_panel = Panel(
        banner_content,
        box=DOUBLE,
        style="bright_magenta",
        padding=(1, 2),
        title="[bold bright_white]Welcome[/bold bright_white]",
        title_align="center"
    )
    
    console.print()
    console.print(banner_panel, justify="center")
    console.print()

def print_menu():
    """Print the main menu using rich"""
    # Print title above the menu
    console.print("\n[bold bright_cyan]SELECT AN OPTION[/bold bright_cyan]", justify="center")
    
    # Create a table for the menu without panel box
    menu_table = Table(show_header=False, box=ROUNDED, style="cyan")
    menu_table.add_column("Option", style="bold bright_blue", width=30)
    
    menu_table.add_row("1.Resize Video")
    menu_table.add_row("2.Split Video")
    menu_table.add_row("3.Crop Video (Social Media)")
    menu_table.add_row("4.List Videos")
    menu_table.add_row("5.Exit")
    
    console.print(menu_table, justify="center")

def list_video_files():
    """List all video files in the current directory"""
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.m4v']
    video_files = []
    
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_files.append(file)
    
    if video_files:
        console.print("\n📁 Available Video Files:", style="bold green")
        
        # Create a table for video files
        files_table = Table(show_header=True, box=ROUNDED, style="cyan")
        files_table.add_column("No.", style="bold blue", width=5)
        files_table.add_column("File Name", style="bright_white")
        files_table.add_column("Size (MB)", style="yellow", justify="right")
        
        for i, file in enumerate(video_files, 1):
            file_size = os.path.getsize(file) / (1024 * 1024)  # Size in MB
            files_table.add_row(str(i), file, f"{file_size:.1f}")
        
        files_panel = Panel(
            files_table,
            title="[bold bright_green]Video Files[/bold bright_green]",
            box=ROUNDED,
            style="green"
        )
        console.print(files_panel)
        return video_files
    else:
        console.print("⚠️  No video files found in current directory!", style="bold yellow")
        return []

def get_video_info(file_path):
    """Get video information using ffprobe"""
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        
        width = video_stream['width']
        height = video_stream['height']
        duration = float(probe['format']['duration'])
        
        return {
            'width': width,
            'height': height,
            'duration': duration,
            'resolution': f"{width}x{height}"
        }
    except Exception as e:
        console.print(f"❌ Error getting video info: {str(e)}", style="bold red")
        return None

def resize_video():
    """Resize video functionality"""
    # Create header panel
    header_panel = Panel(
        "📐 VIDEO RESIZE MODE",
        style="bold magenta",
        box=HEAVY,
        title_align="center"
    )
    console.print(header_panel)
    
    video_files = list_video_files()
    if not video_files:
        return
    
    # Select video file
    try:
        choice = IntPrompt.ask(f"\n[cyan]Select video file[/cyan]", choices=[str(i) for i in range(1, len(video_files)+1)]) - 1
        
        input_file = video_files[choice]
        console.print(f"✅ Selected: [green]{input_file}[/green]")
        
        # Get current video info
        info = get_video_info(input_file)
        if not info:
            return
        
        console.print(f"📊 Current Resolution: [blue]{info['resolution']}[/blue]")
        
        # Show resize options
        resize_options = {
            '1': ('1920x1080', 'Full HD'),
            '2': ('1280x720', 'HD'),
            '3': ('854x480', 'SD'),
            '4': ('640x360', 'Low'),
            '5': ('custom', 'Custom Size')
        }
        
        # Create resize options table
        resize_table = Table(show_header=True, box=ROUNDED, style="cyan")
        resize_table.add_column("Option", style="bold blue", width=8)
        resize_table.add_column("Name", style="bright_white")
        resize_table.add_column("Resolution", style="yellow")
        
        for key, (resolution, name) in resize_options.items():
            resize_table.add_row(key, name, resolution)
        
        resize_panel = Panel(
            resize_table,
            title="[bold bright_cyan]📐 Resize Options[/bold bright_cyan]",
            box=ROUNDED,
            style="cyan"
        )
        console.print(resize_panel)
        
        resize_choice = Prompt.ask("\n[cyan]Select resize option[/cyan]", choices=['1', '2', '3', '4', '5'])
        
        if resize_choice == '5':
            width = Prompt.ask("[cyan]Enter width[/cyan]")
            height = Prompt.ask("[cyan]Enter height[/cyan]")
            target_resolution = f"{width}x{height}"
        elif resize_choice in resize_options:
            target_resolution = resize_options[resize_choice][0]
        else:
            console.print("❌ Invalid option!", style="bold red")
            return
        
        # Generate output filename
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_resized_{target_resolution.replace('x', '_')}{ext}"
        
        console.print(f"\n🔄 Resizing video to [yellow]{target_resolution}[/yellow]...")
        console.print(f"📤 Output: [blue]{output_file}[/blue]")
        
        # Resize video using ffmpeg with progress
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Resizing video...", total=None)
                
                (
                    ffmpeg
                    .input(input_file)
                    .filter('scale', target_resolution)
                    .output(output_file, vcodec='libx264', acodec='copy')
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                
            console.print("✅ Video resized successfully!", style="bold green")
            
            # Show new file info
            new_info = get_video_info(output_file)
            if new_info:
                new_size = os.path.getsize(output_file) / (1024 * 1024)
                console.print(f"📊 New file: [green]{output_file}[/green] ([yellow]{new_size:.1f} MB[/yellow], [blue]{new_info['resolution']}[/blue])")
                
        except ffmpeg.Error as e:
            console.print(f"❌ Error resizing video: {e.stderr.decode() if e.stderr else str(e)}", style="bold red")
        
    except ValueError:
        console.print("❌ Please enter a valid number!", style="bold red")
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user", style="bold yellow")

def split_video():
    """Split video functionality"""
    # Create header panel
    header_panel = Panel(
        "✂️  VIDEO SPLIT MODE",
        style="bold magenta",
        box=HEAVY,
        title_align="center"
    )
    console.print(header_panel)
    
    video_files = list_video_files()
    if not video_files:
        return
    
    try:
        # Select video file
        choice = IntPrompt.ask(f"\n[cyan]Select video file[/cyan]", choices=[str(i) for i in range(1, len(video_files)+1)]) - 1
        
        input_file = video_files[choice]
        console.print(f"✅ Selected: [green]{input_file}[/green]")
        
        # Get video info
        info = get_video_info(input_file)
        if not info:
            return
        
        duration_minutes = info['duration'] / 60
        console.print(f"📊 Video Duration: [blue]{duration_minutes:.2f} minutes ({info['duration']:.2f} seconds)[/blue]")
        
        # Create split options table
        split_table = Table(show_header=True, box=ROUNDED, style="cyan")
        split_table.add_column("Option", style="bold blue", width=8)
        split_table.add_column("Duration", style="bright_white")
        
        split_table.add_row("1", "10 seconds per segment")
        split_table.add_row("2", "30 seconds per segment")
        split_table.add_row("3", "1 minute per segment")
        split_table.add_row("4", "2 minutes per segment")
        split_table.add_row("5", "Custom duration")
        
        split_panel = Panel(
            split_table,
            title="[bold bright_cyan]⏱️  Split Options[/bold bright_cyan]",
            box=ROUNDED,
            style="cyan"
        )
        console.print(split_panel)
        
        duration_choice = Prompt.ask("\n[cyan]Select split option[/cyan]", choices=['1', '2', '3', '4', '5'])
        
        duration_map = {'1': 10, '2': 30, '3': 60, '4': 120}
        
        if duration_choice in duration_map:
            segment_duration = duration_map[duration_choice]
        elif duration_choice == '5':
            segment_duration = float(Prompt.ask("[cyan]Enter duration in seconds[/cyan]"))
        else:
            console.print("❌ Invalid option!", style="bold red")
            return
        
        # Create segments directory
        segments_dir = "segments"
        if not os.path.exists(segments_dir):
            os.makedirs(segments_dir)
        
        name = os.path.splitext(input_file)[0]
        output_prefix = f"{segments_dir}/{name}_segment"
        
        # Calculate expected segments
        expected_segments = int(info['duration'] / segment_duration) + (1 if info['duration'] % segment_duration > 0 else 0)
        
        console.print(f"\n🔄 Splitting video into [yellow]{expected_segments}[/yellow] segments of [blue]{segment_duration}[/blue] seconds each...")
        console.print(f"📁 Output directory: [green]{segments_dir}[/green]")
        
        # Split the video with progress
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Splitting video...", total=None)
                
                # Use the split function from split_video.py
                from split_video import split_video_ffmpeg_python
                split_video_ffmpeg_python(input_file, output_prefix, segment_duration)
            
            console.print("✅ Video split successfully!", style="bold green")
            
        except Exception as e:
            console.print(f"❌ Error splitting video: {str(e)}", style="bold red")
            
    except ValueError:
        console.print("❌ Please enter a valid number!", style="bold red")
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user", style="bold yellow")

def crop_video():
    """Crop video functionality for social media platforms"""
    # Create header panel
    header_panel = Panel(
        "✂️  VIDEO CROP MODE (Social Media)",
        style="bold magenta",
        box=HEAVY,
        title_align="center"
    )
    console.print(header_panel)
    
    video_files = list_video_files()
    if not video_files:
        return
    
    # Select video file
    try:
        choice = int(Prompt.ask(f"\n[cyan]Select video file (1-{len(video_files)})[/cyan]")) - 1
        if choice < 0 or choice >= len(video_files):
            console.print("❌ Invalid selection!", style="bold red")
            return
        
        input_file = video_files[choice]
        console.print(f"✅ Selected: [green]{input_file}[/green]")
        
        # Get current video info
        info = get_video_info(input_file)
        if not info:
            return
        
        console.print(f"📊 Current Resolution: [blue]{info['resolution']}[/blue]")
        
        # Show crop options for different social media platforms
        crop_options = {
            '1': ('1080:1920', 'TikTok/Instagram Stories (9:16)'),
            '2': ('1080:1080', 'Instagram Post (1:1)'),
            '3': ('1200:630', 'Facebook Post (1.91:1)'),
            '4': ('1080:608', 'YouTube Thumbnail (16:9)'),
            '5': ('1080:1350', 'Instagram Feed (4:5)'),
            '6': ('custom', 'Custom Crop')
        }
        
        # Create crop options table
        crop_table = Table(show_header=True, box=ROUNDED, style="cyan")
        crop_table.add_column("Option", style="bold blue", width=8)
        crop_table.add_column("Platform", style="bright_white")
        crop_table.add_column("Aspect Ratio", style="yellow")
        
        for key, (ratio, platform) in crop_options.items():
            crop_table.add_row(key, platform, ratio if ratio != 'custom' else 'Custom')
        
        crop_panel = Panel(
            crop_table,
            title="[bold bright_cyan]✂️  Crop Options[/bold bright_cyan]",
            box=ROUNDED,
            style="cyan"
        )
        console.print(crop_panel)
        
        crop_choice = Prompt.ask("\n[cyan]Select crop option[/cyan]", choices=['1', '2', '3', '4', '5', '6'])
        
        if crop_choice == '6':
            width = int(Prompt.ask("[cyan]Enter crop width[/cyan]"))
            height = int(Prompt.ask("[cyan]Enter crop height[/cyan]"))
            platform_name = "Custom"
        elif crop_choice in crop_options:
            ratio, platform_name = crop_options[crop_choice]
            width, height = ratio.split(':')
            width, height = int(width), int(height)
            
            # Get video info to check dimensions
            video_info = get_video_info(input_file)
            if video_info:
                input_width = int(video_info['width'])
                input_height = int(video_info['height'])
                
                # If crop dimensions are larger than input, scale them down while maintaining aspect ratio
                if width > input_width or height > input_height:
                    # Calculate scale factor to fit within input dimensions
                    scale_w = input_width / width
                    scale_h = input_height / height
                    scale = min(scale_w, scale_h)
                    
                    width = int(width * scale)
                    height = int(height * scale)
                    
                    console.print(f"⚠️  [yellow]Crop dimensions scaled down to {width}x{height} to fit input video[/yellow]")
        else:
            console.print("❌ Invalid option!", style="bold red")
            return
        
        # Generate output filename with proper sanitization
        name, ext = os.path.splitext(input_file)
        
        # Create a clean platform name for filename
        if crop_choice == '1':
            clean_platform = "tiktok_stories_9x16"
        elif crop_choice == '2':
            clean_platform = "instagram_post_1x1"
        elif crop_choice == '3':
            clean_platform = "facebook_post_1_91x1"
        elif crop_choice == '4':
            clean_platform = "youtube_thumbnail_16x9"
        elif crop_choice == '5':
            clean_platform = "instagram_feed_4x5"
        else:
            clean_platform = "custom"
        
        output_file = f"{name}_cropped_{clean_platform}{ext}"
        
        console.print(f"\n🔄 Cropping video for [yellow]{platform_name}[/yellow]...")
        console.print(f"📤 Output: [blue]{output_file}[/blue]")
        
        # Crop video using ffmpeg with progress
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Cropping video...", total=None)
                
                # Use the correct FFmpeg crop filter format with audio copy
                (
                    ffmpeg
                    .input(input_file)
                    .filter('crop', int(width), int(height), f'(iw-{width})/2', f'(ih-{height})/2')
                    .output(output_file, vcodec='libx264', acodec='copy')
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                
            console.print("✅ Video cropped successfully!", style="bold green")
            
            # Show new file info
            new_info = get_video_info(output_file)
            if new_info:
                new_size = os.path.getsize(output_file) / (1024 * 1024)
                console.print(f"📊 New file: [green]{output_file}[/green] ([yellow]{new_size:.1f} MB[/yellow], [blue]{new_info['resolution']}[/blue])")
                
        except ffmpeg.Error as e:
            console.print(f"❌ Error cropping video: {e.stderr.decode() if e.stderr else str(e)}", style="bold red")
        
    except ValueError:
        console.print("❌ Please enter a valid number!", style="bold red")
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user", style="bold yellow")

def main():
    """Main program loop"""
    try:
        while True:
            print_banner()
            print_menu()
            
            try:
                choice = Prompt.ask("\n[cyan bold]Enter your choice[/cyan bold]", choices=['1', '2', '3', '4', '5'])
                
                if choice == '1':
                    resize_video()
                elif choice == '2':
                    split_video()
                elif choice == '3':
                    crop_video()
                elif choice == '4':
                    list_video_files()
                elif choice == '5':
                    console.print("\n👋 Thanks for using Video Terminal Tool! Goodbye!", style="bold green")
                    break
                
                if choice in ['1', '2', '3', '4']:
                    Prompt.ask("\n[cyan]Press Enter to continue...[/cyan]", default="")
                    console.clear()  # Clear screen
                    
            except KeyboardInterrupt:
                console.print("\n⚠️  Operation cancelled by user", style="bold yellow")
                choice = Prompt.ask("[cyan]Do you want to exit? (y/n)[/cyan]", choices=['y', 'n'], default='n')
                if choice.lower() == 'y':
                    break
                console.clear()
                
    except Exception as e:
        console.print(f"❌ Unexpected error: {str(e)}", style="bold red")

if __name__ == "__main__":
    # Check if ffmpeg is available
    try:
        ffmpeg.probe("dummy")  # This will fail but test if ffmpeg is available
    except ffmpeg.Error:
        pass  # Expected error, ffmpeg is available
    except FileNotFoundError:
        console.print("❌ Error: FFmpeg not found! Please install FFmpeg first.", style="bold red")
        console.print("💡 Install FFmpeg from: https://ffmpeg.org/download.html", style="bold yellow")
        sys.exit(1)
    
    main()